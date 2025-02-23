'''
Implements the Submodule class for the trends agent.
Reads trends_search_terms from params or environment variable TRENDS_SEARCH_TERMS.
Uses pytrends to get trends data, then uses LangChain and OpenAI to generate insights.
If useful insights are found, calls the message agent to send a report.
'''

import os
import json
from pytrends.request import TrendReq
from langchain_core.runnables import RunnableSequence
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from .Submodule import Submodule
from datetime import datetime, timedelta

class Trends(Submodule):
	"""
	Submodule that analyzes trend data using pytrends and generates insights using OpenAI.
	"""
	def run(self):
		"""
		Analyze trends for specified search terms and generate insights.
		If useful insights are found, call the message agent.
		"""
		# Read search terms from params or environment variable
		search_terms = self.params.get('trends_search_terms')
		if search_terms is None:
			env_terms = os.getenv('TRENDS_SEARCH_TERMS')
			if env_terms:
				try:
					search_terms = json.loads(env_terms)
				except json.JSONDecodeError:
					self.logger.error("TRENDS_SEARCH_TERMS is not a valid JSON array")
					return
			else:
				self.logger.error("No search terms provided and TRENDS_SEARCH_TERMS not set")
				return

		timeframes = {
		#	'last_week': (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')+" "+datetime.now().strftime('%Y-%m-%d'),
			'last_month': (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')+" "+datetime.now().strftime('%Y-%m-%d'),
		#	'last_year': (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')+" "+datetime.now().strftime('%Y-%m-%d')
		}
		if not isinstance(search_terms, list):
			self.logger.error("search_terms should be a list")
			return

		# Initialize pytrends
		pytrends = TrendReq(hl='US', tz=0)

		# Get trends data for last week, last month, and last year
		trends_data = {}
		

		for timeframe_name, timeframe_value in timeframes.items():
			try:
				self.logger.debug(f"Fetching trends for {timeframe_name} with timeframe {timeframe_value}")
				pytrends.build_payload(
					kw_list=search_terms,
					timeframe=timeframe_value,
					geo='',
					gprop='',
					cat=self.params.get('cat', 0)
					)
				trends_data[timeframe_name] = pytrends.interest_over_time()
			except Exception as e:
				self.logger.error(f"Failed to fetch trends for {timeframe_name}: {str(e)}")
	

		# Format trends data for the prompt
		# Convert timestamps to strings in the dictionary
		trends_str=""
		for timeframe, df in trends_data.items():
			if not df.empty:
				trends_str += "# Trends data for {timeframe}:\n"
				data_dict = df.to_dict()
				# Convert to markdown table
				for term, term_data in data_dict.items():
					if term == "isPartial":
						continue
					trends_str += f"## {term} (source: https://www.google.com/trends/explore#q={term}&cat={self.params.get('cat', 0)})\n"
					for timestamp, value in term_data.items():
						trends_str += f"| {str(timestamp)} | {value} |\n"
				self.logger.info(f"{trends_str}")

		# Set up LangChain and OpenAI
		# Note: Ensure OPENAI_API_KEY is set in the environment
		GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
		
		try:
			json_schema = {
				"title": "trend_insights",
				"description": "Insights generated from trends data",
				"type": "object",
				"properties": {
					"is_relevant": {
						"type": "boolean",
						"description": "Does the response contain relevant insights?",
					},
					"insight": {
						"type": "string",
						"description": "The useful insights extracted from the trends data",
					},
				},
				"required": ["is_relevant", "insight"],
			}

			llm = ChatOpenAI(
				model="gpt-4o",
				api_key=GITHUB_TOKEN,
				base_url="https://models.inference.ai.azure.com"
			)
			structured_llm = llm.with_structured_output(json_schema)
			prompt_template = ChatPromptTemplate.from_messages([
				("system", f"""
**Task:** Generate insights from trends data.
Your task is to generate insights from the trends data provided below.
Determine if the trends are relevant and provide any useful insights.
1. is_relevant: True/False. Consider the trend relevant only if it has a significant change.
2. insight: The useful insights extracted from the trends data (if any). Add any relevant links as source if provided.
"""),
				("user", """
**Trends Data:**
{trends_data}
				""")
			])
			chain = prompt_template | structured_llm
			response = chain.invoke({"trends_data": trends_str})
			self.logger.info(f"Response: {response}")
		except Exception as e:
			self.logger.error(f"Failed to generate insights: {str(e)}")
			return

		# Check if insights are useful
		if response.get('is_relevant', False):
			message = f"{response.get('insight', 'No insights provided')}"
			self.logger.info(message)
			# Call the message agent to send a report
			return message
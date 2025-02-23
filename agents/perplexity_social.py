'''
Implements the Submodule class for the perplexity social agent.
Use perplexity api to get social media data of last week on the search terms provided
Generate a comprehensive report.
Usage:
python a-link.py '{"agent": "perplexity_social", "params": {"search_terms":["covid", "vaccine"]}}'
'''

from datetime import datetime
import json
import re
from .Submodule import Submodule
import os
from langchain_core.runnables import RunnableSequence
from langchain_community.chat_models import ChatPerplexity
from langchain.prompts import ChatPromptTemplate

class Perplexity_social(Submodule):
	"""
	Submodule that analyzes trend on socials using perplexity API.
	"""
	def run(self):
		"""
		Analyze trends for specified search terms and generate insights.
		If useful insights are found, call the message agent.
		"""
		# Read search terms from params or environment variable
		search_terms = self.params.get('search_terms')
		if search_terms is None:
			env_terms = os.getenv('SEARCH_TERMS')
			if env_terms:
				try:
					search_terms = json.loads(env_terms)
				except json.JSONDecodeError:
					self.logger.error("SEARCH_TERMS is not a valid JSON array")
					return
			else:
				self.logger.error("No search terms provided and SEARCH_TERMS not set")
				return
		
		# Initialize perplexity
		llm = ChatPerplexity(
			model="sonar-reasoning-pro",
			api_key=os.getenv("PERPLEXITY_API_KEY"),
		)
		prompt_template = ChatPromptTemplate.from_messages([
			("system", f"""
**Task:** Generate report from last week news and events for the search terms provided by the user.
Your task is to generate a comprehensive report on the last week news and events for the search terms provided by the user.
- Search the social media and the web for the terms provided and other related terms and list all relevant news and opinions
- if no no relevant news or opinions are found on a specific search term, skip it
- current date is {datetime.now().strftime('%Y-%m-%d')}
- don't include any preambles or conclusions
- include sources links in the output
"""),
				("user", """
**search terms:**
{search_terms}
				""")
			])
		chain = prompt_template | llm
		response = chain.invoke({"search_terms": ', '.join(search_terms)})
		message = response.content
		# remove <think> ... </think> tags and everithing in between
		message = re.sub(r'<think>.*?</think>\n\n', '', message, flags=re.DOTALL)
		self.logger.info(f"{message}")
		return message
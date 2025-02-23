'''
Use perplexity_social agent to get social media data of last week on the search terms provided then write some tweets about it.
Usage:
python a-link.py '{"agent": "weekly_x", "params": {"search_terms":["covid", "vaccine"]}}'
'''

from datetime import datetime
import json
import re
from .Submodule import Submodule
from .message import Message
import os
from langchain_core.runnables import RunnableSequence
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
import importlib

class Weekly_x(Submodule):
	"""
	Submodule that uses perplexity_social agent to get data about last news and trend and writes tweet about it.
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
		
		agent = "perplexity_social"
		params = {"search_terms": search_terms}

		# Dynamically import the submodule from the agents folder
		module_name = f'agents.{agent}'
		try:
			module = importlib.import_module(module_name)
		except ImportError as e:
			raise ValueError(f"Could not import module for agent '{agent}': {e}")

		# Assume the class name is the capitalized agent name
		class_name = agent.capitalize()
		try:
			submodule_class = getattr(module, class_name)
		except AttributeError:
			raise ValueError(f"Class '{class_name}' not found in module '{module_name}'")

		# Instantiate the submodule, passing params and process_request for recursive calls
		instance = submodule_class(params, self.process_request)
		context = instance.run()
		if not context:
			self.logger.error("No context returned by submodule")
			return

		llm = ChatOpenAI(
			model="gpt-4o",
			api_key=os.getenv("GITHUB_TOKEN"),
			base_url="https://models.inference.ai.azure.com"
		)
		# Write X about the data
		json_schema = {
			"title": "tweets",
			"description": "Generated X posts (Tweets) about the data retrieved from perplexity_social agent",
			"type": "object",
			"properties": {
				"posts": {
					"type": "array",
					"description": "Array of X posts (Tweets)",
					"items": {
						"type": "string",
						"description": "A X post (Tweet) about the data retrieved from perplexity_social agent",
					},
				},

			},
			"required": ["posts"],
		}
		structured_llm = llm.with_structured_output(json_schema)
		prompt = ChatPromptTemplate.from_messages([
			("system", f"""
You're a cheerful social media expert tasked with capturing your audience's attention.
Write engaging X posts (Tweets) about the provided context.
Use the following guidelines to craft your posts:
- Opens with a fun, attention-grabbing hook.
- Uses informal language and a couple of well-placed emojis.
- Includes a call-to-action or question to invite conversation.
- Remains concise (under 280 characters) while radiating warmth and positivity.
- Never use hashtags.
- Add source links if possible.
"""),
			("user", f"""
**Context:**
{context}
			""")
		])
		chain = prompt | structured_llm
		response = chain.invoke({"data": context})
		self.logger.info(f"Response: {response}")
		for post in response.get('posts', []):
			Message({"message": post}, self.process_request).run()
		return response.get('posts', [])



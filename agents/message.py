'''
Implements the Submodule class for the message agent.
Takes a message from params and prints it to standard output.
'''

from .Submodule import Submodule
import os
import telegram
import asyncio

class Message(Submodule):
	"""
	Submodule that prints a message to standard output and send it to telegram.
	"""
	bot_token = None
	chat_id = None

	def __init__(self, *args, **kwargs):
		self.bot_token = os.environ.get("TELEGRAM_BOT_TOKEN", None)
		self.chat_id = os.environ.get("TELEGRAM_CHAT_ID", None)
		super().__init__(*args, **kwargs)

	async def send(self, message):
		if self.bot_token is not None and self.chat_id is not None:
			bot = telegram.Bot(token=self.bot_token)
			await bot.sendMessage(chat_id=self.chat_id, text=message)
			self.logger.debug(f"Sent message to telegram: {message}")
	
		else:
			print(message)
		
	def run(self):
		"""
		Print the message from params to stdout and log the action to stderr.
		"""
		message = self.params['message']
		asyncio.run(self.send(message)) 


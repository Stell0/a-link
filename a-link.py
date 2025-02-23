'''
A python application that accepts a JSON as parameters, specifying a submodule to call and its arguments.
Each submodule is located in the "agents" folder and implements the Submodule class.

Usage: python a-link.py '<json>'

Sample JSON:
{
	"agent": "message",
	"params": {
		"message": "The message to send"
	}
}
'''

import sys
import json
import importlib
import os

def process_request(json_data):
	"""
	Process the JSON input, load the specified submodule, and execute it.

	Args:
		json_data (str or dict): JSON string or dictionary containing 'agent' and 'params'.

	Returns:
		The result from the submodule's run method.
	"""
	if isinstance(json_data, str):
		data = json.loads(json_data)
	else:
		data = json_data
	agent = data['agent']
	params = data['params']

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
	instance = submodule_class(params, process_request)
	return instance.run()

def list_agents():
	"""
	List all available agents in the agents directory.
	"""
	agents_dir = os.path.join(os.path.dirname(__file__), 'agents')
	agents = []
	for file in os.listdir(agents_dir):
		if file.endswith('.py') and not 'Submodule.py' in file:
			agents.append(file[:-3])
	return agents

if __name__ == '__main__':
	if len(sys.argv) != 2:
		print("Usage: python a-link.py '<json>'")
		sys.exit(1)

	json_str = sys.argv[1]
	try:
		result = process_request(json_str)
		# Depending on the submodule, the result might need handling
		# For now, since some submodules print to stdout or log to stderr, we can exit
	except Exception as e:
		print(f"Error: {str(e)}", file=sys.stderr)
		sys.exit(1)
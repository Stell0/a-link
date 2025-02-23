'''
The base Submodule class that all agent submodules should inherit from.
It provides initialization with params and a process_request function,
and requires implementation of the run method.
'''

import logging
import sys

class Submodule:
    """
    Base class for all submodules, providing common functionality like logging.

    Attributes:
        params (dict): Parameters passed to the submodule.
        process_request (function): Function to call a-link recursively.
        logger (logging.Logger): Logger configured to output to stderr.
    """
    def __init__(self, params, process_request):
        """
        Initialize the submodule.

        Args:
            params (dict): Parameters for the submodule.
            process_request (function): Function to call a-link recursively.
        """
        self.params = params
        self.process_request = process_request
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler(sys.stderr)
        self.logger.addHandler(handler)

    def run(self):
        """
        Abstract method that must be implemented by subclasses.

        Raises:
            NotImplementedError: If not implemented by subclass.
        """
        raise NotImplementedError
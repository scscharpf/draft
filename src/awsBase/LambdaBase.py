import logging
from abc import abstractmethod


class LambdaBase(object):

    def __init__(self, log_level=logging.INFO):
        self.logger = logging.getLogger()
        self.logger.setLevel(log_level)

    @classmethod
    def get_handler(cls, *args, **kwargs):
        def handler(event, context):
            return cls(*args, **kwargs).handle(event, context)
        return handler

    @abstractmethod
    def handle(self, event, context):
        raise NotImplementedError

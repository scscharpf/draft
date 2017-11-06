import logging

from src.awsBase.LambdaBase import LambdaBase


class ClientRestHandler(LambdaBase):

    def __init__(self, s3, log_level=logging.INFO):
        super(ClientRestHandler, self).__init__(log_level)
        self.s3 = s3

    def handle(self, event, context):
        raise NotImplementedError

    @staticmethod
    def _get_bucket_name(event):
        return event['pathParameters']['bucket']

    @staticmethod
    def _get_object_name(event):
        return event['pathParameters']['object']

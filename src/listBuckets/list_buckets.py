import json

import boto3

from src.restHandlers.client_rest_handler import ClientRestHandler


class S3Buckets(ClientRestHandler):

    def __init__(self, s3):
        super(S3Buckets, self).__init__(s3)
        # self.env_bucket = os.getenv("S3_BUCKET")

    def handle(self, event, context):
        self.logger.info('EVENT {}'.format(event))
        buckets_response = self.s3.list_buckets()
        buckets = [bucket['Name'] for bucket in buckets_response['Buckets']]
        self.logger.info('BUCKETS {}'.format(buckets))
        json_response = {'Buckets': buckets}
        return {
                "statusCode": 200,
                "body": json.dumps(json_response)
            }

    # def list_buckets(self):
    #     # s3 = boto3.client('s3')
    #     response = self.s3.list_buckets
    #     buckets = [bucket['Name'] for bucket in response['Buckets']]
    #     self.logger.info('BUCKETS {}'.format(buckets))
    #     print(buckets)
    #     return buckets

handler = S3Buckets.get_handler(boto3.client('s3'))


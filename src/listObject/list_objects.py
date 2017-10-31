import json

import boto3

from src.restHandlers.client_rest_handler import ClientRestHandler


class S3Objects(ClientRestHandler):

    def __init__(self, s3):
        super(S3Objects, self).__init__(s3)
        # self.env_bucket = os.getenv("S3_BUCKET")

    def handle(self, event, context):
        s3resource = boto3.resource('s3')
        bucket_name = self._get_bucket_name(event)
        self.logger.info('Bucket_name {}'.format(bucket_name))
        bucket = s3resource.Bucket(bucket_name)
        response = bucket.objects.all()
        objects_keys = []
        for key in response:
            objects_keys.append(key.key)
        json_response = {'Bucket': bucket_name, 'Files': objects_keys}
        return{
            "statusCode": 200,
            "body": json.dumps(json_response)
        }

handler = S3Objects.get_handler(boto3.client('s3'))


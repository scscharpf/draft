import json

import boto3

from src.restHandlers.client_rest_handler import ClientRestHandler


class S3Object(ClientRestHandler):

    def __init__(self, s3):
        super(S3Object, self).__init__(s3)
    # self.env_bucket = os.getenv("S3_BUCKET")

    def handle(self, event, context):
        s3resource = boto3.resource('s3')
        bucket_name = self._get_bucket_name(event)
        object_name = self._get_object_name(event)
        self.logger.info('Bucket_name {}'.format(bucket_name))
        self.logger.info('Object_name {}'.format(object_name))
        obj = s3resource.Bucket(bucket_name).Object(object_name)
        url = self.s3.generate_presigned_url('get_object', {
            'Bucket': bucket_name,
            'Key': object_name
        })
        json_response = {
                 'key':  obj.key,
                 'status': 'downloaded',
                 'Last modified': format(obj.last_modified)
        }
        return{
            "statusCode": 302,
            "body": json.dumps(json_response),
            "headers": {'location': url}
        }


handler = S3Object.get_handler(boto3.client('s3'))

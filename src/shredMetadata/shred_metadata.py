import json
import logging
import uuid

import boto3
import xarray

from src.awsBase.LambdaBase import LambdaBase


def get_bucket_name(record):
    return record['s3']['bucket']['name']


def get_object_key(record):
    return record['s3']['object']['key']


def get_forecast_date(data_set):
    return str(data_set.data_vars['issue_time'].values)


def get_properties_geojson(data_set):
    return json.loads(data_set.attrs['core_geographic_area_shape'])


def get_data_set(bucket_name, object_key):
    tmp_file_path = '/tmp/' + uuid.uuid4().get_hex()
    boto3.resource('s3').Bucket(bucket_name).download_file(object_key, tmp_file_path)
    return xarray.open_dataset(tmp_file_path)


class MetadataShredder(LambdaBase):

    def __init__(self, s3, log_level=logging.INFO):
        super(MetadataShredder, self).__init__(log_level)
        self.s3 = s3

    def shred_metadata(self, event):
        metadata = []
        for record in event['Records']:
            bucket_name = get_bucket_name(record)
            key_name = get_object_key(record)
            data_set = get_data_set(bucket_name, key_name)
            self.send_metadata_to_dynamodb_table(data_set,bucket_name, key_name)

            #
            # forecast_date = get_forecast_date(data_set)
            # properties_geojson = get_properties_geojson(data_set)

        #     metadata.append({'Bucket': bucket_name,
        #                      'Key': key_name,
        #                      'Forecast Date': forecast_date,
        #                      'Geojson_properties': {
        #                          'Type': properties_geojson['type'],
        #                          'Coordinates': properties_geojson['coordinates']
        #                      }})
        # self.logger.info('Metadata {}'.format(json.dumps(metadata)))
        # return metadata

    def send_metadata_to_dynamodb_table(self, data_set, bucket_name, key_name):
        dynamodb_client = boto3.client('dynamodb')
        properties_geojson = get_properties_geojson(data_set)
        response = dynamodb_client.put_item(
            TableName='scs_new',
            Item={
                'Metadata': {
                    'uuid': uuid.uuid4().get_hex(),
                    'bucket_name': bucket_name,
                    'key_name': key_name,
                    'forecast_date': get_forecast_date(data_set),
                    'coordinates': properties_geojson['coordinates'],
                    'geo_json': {
                        'type': properties_geojson['type'],
                        'properties':   {
                                    'name': properties_geojson['name']
                        }
                    }
                }
            })
        return json.dumps(response)

    def handle(self, event, context):
        self.shred_metadata(event)
        return ({
            'statusCode': 200,
            'body': 'metadata added to database'
        })

handler = MetadataShredder.get_handler(boto3.client('s3'))

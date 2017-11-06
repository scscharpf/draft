import json
import logging
import uuid
from decimal import Decimal
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


def get_properties_name(data_set):
    return get_properties_geojson(data_set)['crs']['properties']['name']


def get_type(data_set):
    return get_properties_geojson(data_set)['type']


def get_data_set(bucket_name, key_name):
    tmp_file_path = '/tmp/' + uuid.uuid4().get_hex()
    boto3.client('s3').download_file(bucket_name, key_name, tmp_file_path)
    return xarray.open_dataset(tmp_file_path)


def get_coords(data_set):
    coords=[]
    properties_geojson = get_properties_geojson(data_set)

    for coord in properties_geojson['coordinates'][0]:
        latitude = Decimal(str(coord[1]))
        longitude = Decimal(str(coord[0]))
        coords.append([longitude, latitude])
    return coords


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
            self.logger.info('dataset {}'.format(data_set))
            item = self.send_metadata_to_dynamodb_table(data_set, bucket_name, key_name)
            self.logger.info('metadata {}'.format(item))

    @staticmethod
    def send_metadata_to_dynamodb_table(data_set, bucket_name, key_name):
        dynamodb_resource = boto3.resource('dynamodb', region_name='eu-west-1')

        item = {'uuid': str(uuid.uuid4()),
                'bucket_name': bucket_name,
                'key_name': key_name,
                'forecast_date': get_forecast_date(data_set),
                'geo_json': {
                    'type': get_type(data_set),
                    'crs': {
                          'properties': {
                              'name': get_properties_name(data_set)
                          },
                          'coordinates': [get_coords(data_set)]
                    }
                }
                }

        table = dynamodb_resource.Table('scs_metadata')
        table.put_item(Item=item)
        return json.dumps(item)

    def handle(self, event, context):
        self.shred_metadata(event)
        return ({
            'statusCode': 200,
            'body': 'metadata added to database'
        })

handler = MetadataShredder.get_handler(boto3.client('s3'))

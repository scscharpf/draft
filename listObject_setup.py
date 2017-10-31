from setuptools import setup

setup(name='list_objects',
      version='0.1',
      packages=['src',
                'src.listBuckets',
                'src.listBuckets.list_buckets',
                'src.restHandlers.client_rest_handler',
                'src.awsBase.LambdaBase'],
      package_dir= {'src' : 'src'}
      )

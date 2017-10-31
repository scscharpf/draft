from setuptools import setup

setup(name='list_objects',
      version='0.1',
      packages=['src',
                'src.listObject',
                'src.listObject.list_objects',
                'src.restHandlers.client_rest_handler',
                'src.awsBase.LambdaBase']
      )


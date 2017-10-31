from setuptools import setup

setup(name='get_object',
      version='0.1',
      packages=['src',
                'src.getObject',
                'src.getObject.get_object',
                'src.restHandlers.client_rest_handler',
                'src.awsBase.LambdaBase']
      )


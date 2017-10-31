from setuptools import setup

setup(name='shred_metadata',
      version='0.1',
      packages=['src',
                'src.shredMetadata',
                'src.shredMetadata.shred_metadata',
                'src.restHandlers.client_rest_handler',
                'src.awsBase.LambdaBase'],
      package_dir= {'src' : 'src'}
      )

from setuptools import setup

setup(name='list_buckets',
      version='0.1',
      packages=['src',
                'src.listBuckets',
                'src.restHandlers',
                'src.awsBase'],
      packages_dir={'': 'src'}

      )

from setuptools import setup

setup(name='shred_metadata',
      version='0.1',
      packages=['src',
                'src.shredMetadata',
                'src.restHandlers',
                'src.awsBase'],
      install_requires=['netCDF4',
                        'xarray'],
      packages_dir={'': 'src'}
      )

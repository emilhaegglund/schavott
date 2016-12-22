from setuptools import setup

try:
  import numpy
except:
  print('Numpy is required to run installation')

    
setup(name='schavott',
      version='0.3',
      description='Scaffolding and assembly in real-time',
      url='http://github.com/emilhaegglund/schavott',
      author='Emil Haegglund',
      author_email = 'haegglund.emil@gmail.com',
      license='MIT',
      scripts = ['bin/schavott'],
      packages = ['schavott'],
      requires=['python (>=2.7)'],
      install_requires=[
        'pyfasta',
        'h5py>=2.2.0',
        'bokeh',
        'watchdog',
        'numpy'],
      keywords = ['MinION-sequencing', 'Bioinformatics', 'Real-time'],
      download_url = 'https://github.com/emilhaegglund/schavott/tarball/v0.3'
      )

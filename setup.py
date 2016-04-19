from setuptools import setup

try:
  import numpy
except:
  print('Numpy is required to run installation')

    
setup(name='schavott',
      version='0.1',
      description='Scaffolding in real-time',
      url='http://github.com/emilhaegglund/staellning',
      author='Emil Haegglund',
      author_email = 'haegglund.emil@gmail.com',
      scripts = ['bin/schavott'],
      packages = ['schavott'],
      install_requires=[
        'pyfasta',
        'h5py>=2.2.0',
        'bokeh',
        'watchdog',
        'numpy',
        'poretools']
      )

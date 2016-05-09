from setuptools import setup

try:
  import numpy
except:
  print('Numpy is required to run installation')

    
setup(name='schavott',
      version='0.1',
      description='Scaffolding and assembly in real-time',
      url='http://github.com/emilhaegglund/schavott',
      author='Emil Haegglund',
      author_email = 'haegglund.emil@gmail.com',
      scripts = ['bin/schavott', 'bin/schavott-assembly'],
      packages = ['schavott'],
      install_requires=[
        'pyfasta',
        'h5py>=2.2.0',
        'bokeh',
        'watchdog',
        'numpy',
        'poretools']
      )

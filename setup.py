from setuptools import setup, find_packages

setup(
  name = 'tfdebugger',
  packages = find_packages(),
  version = '0.1.1',
  description = 'TensorFlow Debugger',
  author = 'Eric Jang',
  author_email = 'ericjang2004@gmail.com',
  url = 'https://github.com/ericjang/tdb', # use the URL to the github repo
  download_url = 'https://github.com/ericjang/tdb/archive/0.1.tar.gz',
  keywords = ['TDB', 'Deep Learning', 'TensorFlow',  'debugging', 'visualization'], 
  classifiers = [
  'Intended Audience :: Developers',
  'Intended Audience :: Science/Research',
  'Programming Language :: Python'
  ],
  license='Apache 2.0',
  install_requires=['toposort>=1.4']
)

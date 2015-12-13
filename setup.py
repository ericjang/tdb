from distutils.core import setup
setup(
  name = 'tdb',
  packages = ['tdb'], # this must be the same as the name above
  version = '0.1',
  description = 'TensorFlow Debugger',
  author = 'Eric Jang',
  author_email = 'ericjang2004@gmail.com',
  url = 'https://github.com/ericjang/tdb', # use the URL to the github repo
  download_url = 'https://github.com/ericjang/tdb/archive/v0.1.tar.gz',
  keywords = ['Deep Learning', 'TensorFlow',  'debugging', 'visualization'], 
  classifiers = [],
  scripts=['tdb_install.py']
)

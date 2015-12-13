from distutils.core import setup
setup(
  name = 'tdb',
  packages = ['tdb'], # this must be the same as the name above
  version = '0.1',
  description = 'TensorFlow Debugger',
  author = 'Eric Jang',
  author_email = 'ericjang2004@gmail.com',
  url = 'https://github.com/ericjang/tdb', # use the URL to the github repo
  download_url = 'https://github.com/ericjang/tdb/tarball/0.1', # I'll explain this in a second
  keywords = ['Deep Learning', 'TensorFlow',  'debugging', 'visualization'], # arbitrary keywords
  classifiers = [],
)

# download and unzip bower dependencies into tdb_ext folder
# is there a cleaner way to do this?
import urllib
SOURCE_URL = 'https://github.com/ericjang/tdb/releases/download/bower_deps_0.1/bower_components.zip'
urllib.urlretrieve(SOURCE_URL, 'tdb_ext/bower_components.zip')

print('extracting bower deps...')
import zipfile
with zipfile.ZipFile('tdb_ext/bower_components.zip', "r") as z:
    z.extractall("tdb_ext/")

# install the notebook extension
import notebook.nbextensions
notebook.nbextensions.install_nbextension('tdb_ext',user=True)


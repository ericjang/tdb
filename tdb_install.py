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


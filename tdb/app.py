from base64 import b64encode
from ipykernel.comm import Comm 
from IPython import get_ipython
import StringIO
import urllib

_comm=None

def is_notebook():
	iPython=get_ipython()
	if iPython is None or not iPython.config:
		return False
	return 'IPKernelApp' in iPython.config

def connect():
	"""
	establish connection to frontend notebook
	"""
	if not is_notebook():
		print('Python session is not running in a Notebook Kernel')
		return
	
	global _comm

	kernel=get_ipython().kernel
	kernel.comm_manager.register_target('tdb',handle_comm_opened)
	# initiate connection to frontend.
	_comm=Comm(target_name='tdb',data={})
	# bind recv handler
	_comm.on_msg(None)

def send_action(action, params=None):
	"""
	helper method for sending actions
	"""
	data={"msg_type":"action", "action":action}
	if params is not None:
		data['params']=params
	_comm.send(data)

def send_fig(fig,name):
	"""
	sends figure to frontend
	"""
	imgdata = StringIO.StringIO()
	fig.savefig(imgdata, format='png')
	imgdata.seek(0)  # rewind the data
	uri = 'data:image/png;base64,' + urllib.quote(b64encode(imgdata.buf))
	send_action("update_plot",params={"src":uri, "name":name})

# handler messages
def handle_comm_opened(msg):
	# this won't appear in the notebook
	print('comm opened')
	print(msg)
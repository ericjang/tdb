"""
top-level interface methods so user doesn't need to directly construct
a dbsession
"""

import debug_session

# default session
_dbsession=None

def debug(evals,feed_dict=None,breakpoints=None,break_immediately=False,session=None):
	"""
	spawns a new debug session
	"""
	global _dbsession
	_dbsession=debug_session.DebugSession(session)
	return _dbsession.run(evals,feed_dict,breakpoints,break_immediately)

def s():
	"""
	step to the next node in the execution order
	"""
	global _dbsession
	return _dbsession.s()

def c():
	"""
	continue
	"""
	global _dbsession
	return _dbsession.c()

def get_exe_queue():
	global _dbsession
	return _dbsession.get_exe_queue()

def get_value(node):
	global _dbsession
	return _dbsession.get_value(node)
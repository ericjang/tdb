from toposort import toposort, toposort_flatten
from transitive_closure import transitive_closure
import tensorflow as tf

_ops={} # Map<string,tdb.PythonOp>
_placeholder_2_op={} # Map<tf.PlaceholderTensor, tdb.PythonOp>

def add_op(op):
	_ops[op.name]=op
	for t in op.outputs:
		_placeholder_2_op[t]=op

def get_op(placeholder):
	return _placeholder_2_op[placeholder]

def is_htop_out(placeholder):
	# returns True if placeholder is the output of a PythonOp
	return placeholder in _placeholder_2_op

def compute_exe_order(evals):
	deps=compute_node_deps()
	eval_names=[e.name for e in evals]
	tc_deps=transitive_closure(eval_names, deps)
	ordered_names = toposort_flatten(tc_deps)
	return [get_node(name) for name in ordered_names]

def get_node(name):
	"""
	returns HTOp or tf graph element corresponding to requested node name
	"""
	if name in _ops:
		return _ops[name]
	else:
		g=tf.get_default_graph()
		return g.as_graph_element(name)

def register_dbsession(dbsession):
	for op in _ops.values():
		op.set_session(dbsession)

def compute_node_deps():
	"""
	- returns the full dependency graph of ALL ops and ALL tensors
	Map<string,list<string>> where key=node name, values=list of dependency names

	If an Op takes in a placeholder tensor that is the ouput of a PythonOp, 
	we need to replace that Placeholder with the PythonOp.
	"""
	deps={}
	g=tf.get_default_graph()
	for op in g.get_operations():
		d=set([i.name for i in op.control_inputs])
		for t in op.inputs:
			if is_htop_out(t):
				d.add(get_op(t).name)
			else:
				d.add(t.name)
		deps[op.name]=d
		for t in op.outputs:
			deps[t.name]=set([op.name])
	# do the same thing with HTOps
	for op in _ops.values():
		d=set()
		for t in op.inputs:
			if is_htop_out(t):
				d.add(get_op(t).name)
			else:
				d.add(t.name)
		deps[op.name]=d
	return deps

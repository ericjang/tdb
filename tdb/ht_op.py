"""
abstract base class for hypertree Op
"""

class HTOp(object):
	"""
	Abstract class for HyperTree Operation
	"""
	def __init__(self, node_type, i, inputs, outputs):
		"""
		Args:
		node_type: enum type of node
		i: count of specific node type (used to compute name), incremented by constructor functions
		inputs: tf.Tensors
		outputs: tf.Tensors
		"""
		super(HTOp, self).__init__()
		self.node_type=node_type
		self.name=node_type+"_"+repr(i)
		self.session = None
		self.inputs=inputs
		self.outputs=outputs
		
	def set_session(self, debugsession):
		"""
		once nodes compute their designated input and output values
		they need to be able to update the DebugSession cache with the
		feed_dict values for their placeholder tensors.

		However, a DebugSession might not exist upon creation. That is why
		the DebugSession registers itself with all its nodes.

		Args:
		debugsession: instance of DebugSession
		"""
		self.session=debugsession

	def run(self,feed_dict):
		"""
		run produces the output Tensors, if any, of a given Node.
		This is in contrast to TensorFlow
		"""
		raise NotImplementedError('Please implement Node.run() in a subclass')

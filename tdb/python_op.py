
COUNT=0

from ht_op import HTOp
import inspect
import numpy as np
import op_store

def python_op(fn, inputs=None, outputs=None):
	"""
	User-exposed api method for constructing a python_node

	Args:
	fn: python function that computes some np.ndarrays given np.ndarrays as inputs. it can have arbitrary side effects.
	inputs: array of tf.Tensors (optional). These are where fn derives its values from
	outputs: tf.Placeholder nodes (optional). These are constructed by the user (which allows the user to
		plug them into other ht.Ops or tf.Ops). The outputs of fn are mapped to each of the output placeholders.

	raises an Error if fn cannot map
	"""

	# construct a PythonOp and return its TensorNode outputs, if it has one
	global COUNT
	# check outputs
	if not isinstance(outputs,list):
		outputs=[outputs]
	for tensor in outputs:
		if tensor.op.type != 'Placeholder':
			raise TypeError('Output nodes must be Placeholders')
	op=PythonOp('Python', fn, COUNT, inputs, outputs)
	op_store.add_op(op)
	COUNT+=1 
	if outputs:
		return outputs[0]
	else:
		return op

class PythonOp(HTOp):
	"""docstring for PythonOp"""
	def __init__(self, node_type, fn, i, inputs, outputs):
		"""
		constructor. user does not call this.
		"""
		super(PythonOp, self).__init__(node_type, i, inputs, outputs)
		self.fn=fn
		
	def run(self, feed_dict):
		#pdb.set_trace()
		args=tuple(feed_dict[i] for i in self.inputs)
		results=self.fn(self, *args)
		self.cache_values(results)
		return results

	def cache_values(self, results):
		"""
		loads into DebugSession cache
		"""
		if results is None:
			# self.fn was probably only used to compute side effects.
			return
		elif isinstance(results,np.ndarray):
			# fn returns single np.ndarray.
			# re-format it into a list
			results=[results]
		# check validity of fn output
		elif isinstance(results,list):
			if len(results) is not len(self.outputs):
				raise ValueError('Number of output tensors does not match number of outputs produced by function')
		elif isinstance(results,np.number):
			if len(self.outputs) != 1:
				raise ValueError('Fn produces scalar but %d outputs expected' % (len(self.outputs)))
			results=[results]
		# assign each element in ndarrays to corresponding output tensor
		for i,ndarray in enumerate(results):
			self.session._cache_value(self.outputs[i], ndarray)
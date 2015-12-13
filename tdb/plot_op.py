
COUNT=0

from python_op import PythonOp
import app
import inspect
import matplotlib.pyplot as plt
import op_store

def plot_op(fn, inputs=[], outputs=[]):
	"""
	User-exposed api method for constructing a python_node

	Args:
	fn: python function that computes some np.ndarrays given np.ndarrays as inputs. it can have arbitrary side effects.
	inputs: array of tf.Tensors (optional). These are where fn derives its values from
	outputs: tf.Placeholder nodes (optional). These are constructed by the user (which allows the user to
		plug them into other ht.Ops or tf.Ops). The outputs of fn are mapped to each of the output placeholders.

	raises an Error if fn cannot map
	"""
	global COUNT, ht
	# check outputs
	if not isinstance(outputs,list):
		outputs=[outputs]

	for tensor in outputs:
		if tensor.op.type is not 'Placeholder':
			raise Error('Output nodes must be Placeholders')

	op=PlotOp(fn, COUNT, inputs, outputs)

	op_store.add_op(op)
	COUNT+=1 

	# if node has output, return value for python_op is the first output (placeholder) tensor
	# otherwise, return the op
	if outputs:
		return outputs[0]
	else:
		return op

class PlotOp(PythonOp):
	def __init__(self, fn, i, inputs, outputs):
		super(PlotOp, self).__init__('Plot', fn, i, inputs, outputs)
		
	def run(self, feed_dict):
		results=super(PlotOp, self).run(feed_dict)
		# send the image over
		if app.is_notebook():
			fig=plt.gcf()
			app.send_fig(plt.gcf(), self.name)
			# close the figure
			plt.close(fig)
		return results

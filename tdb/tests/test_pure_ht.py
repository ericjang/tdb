"""
Test networks consisting only of hypertree nodes (no TensorFlow nodes)

This replicates the pure-Tensorflow network from test_pure_tf, but implements
the ops as HyperTree PythonOps.
"""

import tensorflow as tf
import unittest
import tdb

def myadd(ctx,a,b):
	"""
	a,b are scalars
	"""
	return a+b
	
def mymult(ctx, a,b):
	"""
	a,b are scalars
	"""
	return a*b

def myneg(ctx, a):
	return -a

def build_graph_ht():
	a=tf.constant(2)
	b=tf.constant(3)
	c=tdb.python_op(myadd,inputs=[a,b],outputs=[tf.placeholder(tf.int32)])
	c2=tdb.python_op(mymult,inputs=[a,b],outputs=[tf.placeholder(tf.int32)])
	d=tdb.python_op(myneg,inputs=[c],outputs=[tf.placeholder(tf.int32)])
	return a,b,c,c2,d

class TestDebuggingHT(unittest.TestCase):
	def test_1(self):
		"""
		See TestDebuggingTF.test_1
		"""
		# construct TensorFlow graph as usual
		a,b,c,c2,d=build_graph_ht()
		evals=[a,b,c,c2,d]
		status,result=tdb.debug(evals, feed_dict=None, breakpoints=None, break_immediately=False)
		self.assertEqual(status, tdb.FINISHED)
		self.assertEqual(result[0],2) # a = 2
		self.assertEqual(result[1],3) # b = 3
		self.assertEqual(result[2],5) # c = 5
		self.assertEqual(result[4],-5) # c2 = -5
		self.assertEqual(result[3],6) # d = 6

	def test_2(self):
		"""
		See TestDebuggingTF.test_2
		"""
		a,b,c,c2,d=build_graph_ht()
		status,result=tdb.debug([c], feed_dict=None, breakpoints=None, break_immediately=True)
		self.assertEqual(status, tdb.PAUSED)
		status,result=tdb.c() # continue
		self.assertEqual(status, tdb.FINISHED)
		self.assertEqual(result[0],5) # check that c = 5

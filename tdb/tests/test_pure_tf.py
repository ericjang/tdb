"""
Headless debugging of HyperTree where nodes only consist of 
TensorFlow nodes
"""

import tensorflow as tf
import unittest
import tdb

def build_graph_tf():
	a=tf.constant(2)
	b=tf.constant(3)
	c=tf.add(a,b)
	c2=tf.mul(a,b)
	d=tf.neg(c)
	return a,b,c,c2,d

class TestDebuggingTF(unittest.TestCase):
	def test_1(self):
		"""
		test debugging of a pure TensorFlow graph
		no breakpoints, all nodes evaluated
		this should automatically build an InteractiveSession for us and create a HyperTree
		"""
		# construct TensorFlow graph as usual
		a,b,c,c2,d=build_graph_tf()
		evals=[a,b,c,c2,d]
		status,result=tdb.debug(evals, feed_dict=None, breakpoints=None, break_immediately=False)
		self.assertEqual(status, tdb.FINISHED)
		self.assertEqual(result[0],2) # a = 2
		self.assertEqual(result[1],3) # b = 3
		self.assertEqual(result[2],5) # c = 5
		self.assertEqual(result[4],-5) # c2 = 6
		self.assertEqual(result[3],6) # d = -5

	def test_2(self):
		"""
		single eval of the pentultimate node
		breka immediately.
		verify that the execution order does NOT contain d or c2
		"""
		a,b,c,c2,d=build_graph_tf()
		status,result=tdb.debug([c], feed_dict=None, breakpoints=None, break_immediately=True)
		self.assertEqual(status, tdb.PAUSED)
		status,result=tdb.c() # continue
		self.assertEqual(status, tdb.FINISHED)
		self.assertEqual(result[0],5) # check that c = 5
	
	def test_3(self):
		"""
		with breakpoints
		"""
		# construct TensorFlow graph as usual
		a,b,c,c2,d=build_graph_tf()
		status,result=tdb.debug(d, feed_dict=None, breakpoints=[c], break_immediately=False)
		self.assertEqual(status, tdb.PAUSED)
		self.assertEqual(result, None)
		status,result=tdb.c()
		self.assertEqual(status, tdb.FINISHED)
		self.assertEqual(result[0],-5)
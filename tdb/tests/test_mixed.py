"""
test heterogenous graph consisting of hypertree and tensorflow nodes

todo - include a graph that uses placeholder nodes for input AND 
has placeholder ops from PythonOps.

cases:

tf op -> ht op
"""



import sys
import tensorflow as tf
import unittest
import tdb

from test_pure_ht import myadd,mymult,myneg

class TestDebuggingMixed(unittest.TestCase):
	def test_1(self):
		"""
		ht->tf
		"""
		a=tf.constant(2)
		b=tf.constant(3)
		c=tdb.python_op(myadd,inputs=[a,b],outputs=[tf.placeholder(tf.int32)]) # a+b
		d=tf.neg(c)
		status,result=tdb.debug([d], feed_dict=None, breakpoints=None, break_immediately=False)	
		self.assertEqual(status, tdb.FINISHED)
		self.assertEqual(result[0],-5)

	def test_2(self):
		"""
		tf -> ht
		"""
		a=tf.constant(2)
		b=tf.constant(3)
		c=tf.add(a,b)
		d=tdb.python_op(myneg,inputs=[c],outputs=[tf.placeholder(tf.int32)])
		status,result=tdb.debug([d], feed_dict=None, breakpoints=None, break_immediately=False)
		self.assertEqual(status, tdb.FINISHED)
		self.assertEqual(result[0],-5)
		self.assertEqual(tdb.get_value(d),-5)
		self.assertEqual(tdb.get_value(d.name),-5)
		
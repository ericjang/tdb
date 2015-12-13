import unittest

import tdb
from tdb.transitive_closure import transitive_closure
from test_pure_tf import build_graph_tf


import tensorflow as tf


"""
testing exe order stuff (topological sorting, transitive_closure, etc.)

to run this test: python -m unittest test_exe_order

"""

class TestExeOrderMethods(unittest.TestCase):
	def test_closure(self):
		"""
		evaluating 8 in this graph does not depend on evaluating 6
		so 6 should be excluded from the closure.
		"""
		G={
			1:{},
			2:{},
			3:{},
			4:{1,2},
			5:{2,3},
			6:{3},
			7:{5},
			8:{4,7}
		}
		T=transitive_closure([8],G)
		for i in [1,2,3,4,5,7,8]:
			self.assertTrue(i in T)
		self.assertFalse(6 in T)
	
	def test_tf(self):
		"""
		ensures that execution ordering is correct
		"""
		build_graph_tf()
		g=tf.get_default_graph()
		for op in g.get_operations():
			print(op.name)
		
		deps=tdb.op_store.compute_node_deps()
		unidict = {k.encode('ascii'): set([v.encode('ascii') for v in s]) for k, s in deps.items()}

		a="Const"
		b="Const_1"
		a0=a+":0"
		b0=b+":0"
		c="Add"
		c0=c+":0"
		d="Mul"
		d0=d+":0"
		e="Neg"
		e0=e+":0"
		target = {
			a:set(),
			b:set(),
			a0:set([a]),
			b0:set([b]),
			c:set([a0,b0]),
			c0:set([c]),
			d:set([a0,b0]),
			d0:set([d]),
			e:set([c0]),
			e0:set([e])
		}
		print("deps")
		print(unidict)
		print("target")
		print(target)
		self.assertEqual(deps,target)

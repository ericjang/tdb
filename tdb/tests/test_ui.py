
import unittest
import tdb

class TestUI(unittest.TestCase):
	def test_1(self):
		# verify that ui is indeed disabled
		self.assertFalse(tdb.is_notebook())

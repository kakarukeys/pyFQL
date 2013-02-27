import unittest
from pyFQL import *

class ExpressionGenerationTests(unittest.TestCase):
	def test_basic_query(self):
		query = status.select(status.status_id, status.message).where(status.status_id == 10151536776980934)
		self.assertEqual(query.expression, "select status_id, message from status where status_id = 10151536776980934")
		
	def test_me_function(self):
		query = friend.select(friend.uid2).where(friend.uid1 == me())
		self.assertEqual(query.expression, "select uid2 from friend where uid1 = me()")

if __name__ == "__main__":
	unittest.main()

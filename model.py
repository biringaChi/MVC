__author__ = 'biringaChi'

from sqlite3 import connect
from contextlib import contextmanager

"""
Accounts Table
++++++++++++++++++++++
id  | Account | Amount
++++++++++++++++++++++
int | int     | int
++++++++++++++++++++++
"""

class AccountDB:
	def __init__(self) -> None:
		self.account_db =  "./db/account_db.db"
	
	def __str__(self) -> str: return self.__class__.__name__
	
	def __repr__(self) -> str: return self.__str__()
	
	@contextmanager
	def account_table(self, curr):
		curr.execute("create table if not exists accounts(id integer PRIMARY KEY, Account integer, Amount integer)")
		try:
			yield
		finally:
			pass
	
	def populate(self):
		with connect(self.account_db) as conn:
			account1 = (83707327, 100000)
			account2 = (97345207, 200000)
			curr = conn.cursor()
			with self.account_table(curr):
				curr.execute("INSERT into accounts(Account, Amount) VALUES(?, ?)", account1)
				curr.execute("INSERT into accounts(Account, Amount) values(?, ?)", account2)
				for row in curr.execute('select Account, Amount from accounts'):
					print(row)
				print("Accounts table created")

# if __name__ == "__main__":
# 	adb = AccountDB() 
# 	adb.populate()
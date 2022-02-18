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
		curr.execute("create table if not exists accounts(id integer PRIMARY KEY, Account integer, Amount real)")
		try:
			yield
		finally:
			pass
	
	def populate(self):
		with connect(self.account_db) as conn:
			account1 = (83707327, 100000.00)
			account2 = (97345207, 200000.00)
			account3 = (90413650, 300000.00)
			account4 = (10788931, 400000.00)
			account5 = (93192708, 500000.00)

			curr = conn.cursor()
			with self.account_table(curr):
				curr.execute("INSERT into accounts(Account, Amount) VALUES(?, ?)", account1)
				curr.execute("INSERT into accounts(Account, Amount) values(?, ?)", account2)
				curr.execute("INSERT into accounts(Account, Amount) values(?, ?)", account3)
				curr.execute("INSERT into accounts(Account, Amount) values(?, ?)", account4)
				curr.execute("INSERT into accounts(Account, Amount) values(?, ?)", account5)
				for row in curr.execute('select * from accounts'): print(row)
				print("Accounts table created")
	
	def response_message(self, transaction, amount, account):
		if transaction.lower().startswith("dep"):
			print(f"${amount} was successfully deposited to {account} account")
		elif transaction.lower().startswith("with"):
			print(f"{amount} was successfully withdrawn from {account} account")
		else: print("Unsuccessfully transaction") 
		
	def update(self, transaction, amount, account):
		"""
		Arguments.  
		withdraw infomrmation is not
			- Amount: type(float)
			- Account: type(int)
			- transaction: type(string)
		"""
		with connect(self.account_db) as conn:
			curr = conn.cursor()
			with self.account_table(curr):
				curr.execute('UPDATE accounts SET amount = ? WHERE Account = ?', (amount, account))
				conn.commit()
				return self.response_message(transaction, amount, account)

	def get_current_balance(self, account):
		with connect(self.account_db) as conn:
			cur = conn.cursor()
			for account_details in cur.execute('select Account, Amount from accounts'):
				account_number = account_details[0]
				amount = account_details[1]
				if account_number == account:
					return amount
				else: raise ValueError("Account not found")
		
	def view(self):
		with connect(self.account_db) as conn:
			curr = conn.cursor()
			with self.account_table(curr):
				for cols in curr.execute('select * from accounts'):
					print(cols)
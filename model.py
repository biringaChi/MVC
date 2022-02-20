__author__ = 'biringaChi'

from sqlite3 import connect
import pandas as pd
from contextlib import contextmanager
from typing import List, Tuple

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
		self.account_db = "./db/account_db.db"
	
	def __str__(self) -> str: return self.__class__.__name__
	
	def __repr__(self) -> str: return self.__str__()
	
	@contextmanager
	def account_table(self, curr) -> None:
		curr.execute("create table if not exists accounts(id integer PRIMARY KEY, Account integer, Amount real)")
		try:
			yield
		finally:
			pass

	def read_data(self) -> Tuple[List]:
		try:
			data = pd.read_csv("data.csv")
		except FileNotFoundError as e:
			raise(e)
		accounts = [account for account in data["Account"]]
		amounts = [amount for amount in data["Amount"]]
		return accounts, amounts 
	
	def populate(self) -> str:
		with connect(self.account_db) as conn:
			curr = conn.cursor()
			with self.account_table(curr):
				accounts, amounts = self.read_data()
				for account, amount in zip(accounts, amounts):
					curr.execute("INSERT into accounts(Account, Amount) VALUES(?, ?)", (account, amount))
				for row in curr.execute('select * from accounts'): print(row)
				print("Accounts table created")
	
	def response_message(self, transaction: str, amount: float, account: int) -> str:
		if transaction.lower().startswith("dep"):
			print(f"${amount} was successfully deposited to {account} account")
		elif transaction.lower().startswith("with"):
			print(f"${amount} was successfully withdrawn from {account} account")
		else: print("Transaction unsuccessful...\nPlease check transaction fields...")

	def get_current_balance(self, account) -> float:
		with connect(self.account_db) as conn:
			cur = conn.cursor()
			cur.execute('SELECT Amount FROM accounts WHERE Account = ?', (account,))
			amount = cur.fetchone()[0]
			if amount is not None:
				return amount
			else:
				raise ValueError("Account not found")
		
	def view(self) -> None:
		with connect(self.account_db) as conn:
			curr = conn.cursor()
			with self.account_table(curr):
				for cols in curr.execute('select * from accounts'):
					print(cols)
	
	def deposit(self, account, amount):
		current_balance = self.get_current_balance(account)
		current_balance += amount
		return float(str("%.2f" % current_balance))
		
	def withdraw(self, account, amount):
		current_balance = self.get_current_balance(account)
		if current_balance < amount:
			raise ValueError("Insufficient funds")
		else: current_balance -= amount
		return float(str("%.2f" % current_balance))

	def update_data(self, transaction: str, account: int, amount: float) -> str:
		"""
		Arguments.  
			- Amount: type(float)
			- Account: type(int)
			- transaction: type(string)
		"""
		with connect(self.account_db) as conn:
			curr = conn.cursor()
			with self.account_table(curr):
				if transaction.lower().startswith("dep"):
					new_balance = self.deposit(account, amount)
					curr.execute('UPDATE accounts SET amount = ? WHERE Account = ?', (new_balance, account))
				elif transaction.lower().startswith("with"):
					try:
						new_balance = self.withdraw(account, amount)
						print("new_balance: ", new_balance)
						curr.execute('UPDATE accounts SET amount = ? WHERE Account = ?', (new_balance, account))
					except:
						print("Withdrawal failed: Insufficient funds...")
						return
				else: ValueError("Please try again")
			conn.commit()
			return self.response_message(transaction, amount, account)

	def get_data(self) -> List[Tuple]:
		data = []
		with connect(self.account_db) as conn:
			for cols in conn.cursor().execute('select Account, Amount from accounts'):
				data.append(cols)
		return data
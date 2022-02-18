__author__ = 'biringaChi'

from model import AccountDB

class Controller(AccountDB):
	def __init__(self) -> None:
		super().__init__()
	
	def __str__(self) -> str: return self.__class__.__name__
	
	def __repr__(self) -> str: return self.__str__()


	def deposit(self, transaction, account, amount):
		current_balance = self.get_current_balance(account)
		current_balance += amount
		self.update(transaction, account, amount)

	def withdrawal(self, transaction, account, amount):
		min_dollars = 5
		current_balance = self.get_current_balance(account)
		if current_balance <= min_dollars:
			raise ValueError("Insufficient funds")
		else: current_balance -= amount
		self.update(transaction, account, amount)
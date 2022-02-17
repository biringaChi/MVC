__author__ = 'biringaChi'

from model import AccountDB
from sqlite3 import connect

class Controller(AccountDB):
	def __init__(self) -> None:
		super().__init__()
	
	def __str__(self) -> str: return self.__class__.__name__
	
	def __repr__(self) -> str: return self.__str__()

	def get_current_balance(self, account):
		with connect(self.account_db) as conn:
			cur = conn.cursor()
			for account_details in cur.execute('select Account, Amount from accounts'):
				account_number = account_details[0]
				amount = account_details[1]
				if account_number == account:
					return amount
				else: raise ValueError("Account not found")

	def persist_data(self, account, amount):
		pass

	def deposit(self, account, amount):
		current_balance = self.get_current_balance(account)
		current_balance += amount
		persisted = self.persist_data(current_balance, account) # persist deposited amount to DB
		if persisted == True:
			print(f"{amount} wwas succesfully deposited!")
		else: raise ValueError("Unsucsessful deposit")

	def withdrawal(self, account, amount):
		min_dollars = 5
		current_balance = self.get_current_balance(account)
		if current_balance <= min_dollars:
			raise ValueError("Insufficient funds")
		else: current_balance -= amount
		persisted = self.persist_data(current_balance, amount)
		if persisted == True:
			print(f"{amount} wwas succesfully withdrawn!")
		else: raise ValueError("Unsucsessful withdrawal")
		

# if __name__ == "__main__":
# 	controller = Controller() 
# 	print(controller.get_current_balance(83707327))
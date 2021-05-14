"""Homework 2, part 1"""


class Account:
    def __init__(self, number, balance):
        self.number = number
        self.__balance = balance

    def _authenitcate(self, pin):
        pass

    def deposit(self, amount):
        pass

    def withdraw(self, amount):
        pass

    def __createTransaction(self, datetime):
        pass


class CurrentAccount(Account):
    def __init__(self, number, balance, interest_rate):
        Account.__init__(self, number, balance)
        self.interest_rate = interest_rate

    def withdraw(self, amount):
        pass

    def apply_interest(self):
        pass


class SavingAccount(Account):
    def __init__(self, number, balance, credit_range):
        Account.__init__(self, number, balance)
        self.__credit_range = credit_range

    def withdraw(self, amount):
        pass


class Customer:
    def __init__(self, name, address, dob, card_number, pin):
        self.name = name
        self.address = address
        self.dob = dob
        self.card_number = card_number
        self.pin = pin

    def verifyPassword(self, password):
        pass


class ATM:
    def __init__(self, location, managedby):
        self.location = location
        self.managedby = managedby

    def identifies(self, customer: Customer):
        pass

    def transactions(self):
        pass


class Bank:
    def __init__(self, code, address, account: Account, atm: ATM):
        self.code = code
        self.address = address
        self.account = account
        self.atm = atm
        self.__revenue = 0

    def __manages(self):
        pass

    def __maintains(self):
        pass

    def _printRevenue(self, revenue_from, revenue_to):
        pass


class ATMTransactions:
    def __init__(self, transaction_id, date, transaction_type, amount, post_balance):
        self.transaction_id = transaction_id
        self.date = date
        self.transaction_type = transaction_type
        self.amount = amount
        self.post_balance = post_balance

    def updates(self, account: Account):
        pass


if __name__ == '__main__':
    account_1 = Account('132931451545EE', 14044.55)
    ATM_1 = ATM("street no. 43", 'manager')
    Bank_1 = Bank('043AAS5', 'bank_address', account_1, ATM_1)
    print(Bank_1.account.number)
    print(Bank_1.atm.location)

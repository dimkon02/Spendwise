from models.transaction import Transaction
from decimal import Decimal
from datetime import date

class FinanceManager:

    def __init__(self):
        self.transactions = []

    def add_transaction(self, transaction: Transaction):
        for existing_transaction in self.transactions:
            if existing_transaction.id == transaction.id:
                raise ValueError("ID is already used.")

        self.transactions.append(transaction)

    def get_transactions(self):
        return self.transactions

    def get_transaction_by_id(self, transaction_id):
        for transaction in self.transactions:
            if transaction_id == transaction.id:
                return transaction
        raise ValueError("Transaction not found.")

    def delete_transaction(self, transaction_id):
        try:
            transaction = self.get_transaction_by_id(transaction_id)
        except ValueError:
            return False
        self.transactions.remove(transaction)
        return True


    def update_transaction(self, transaction_id: int, transaction_amount: Decimal, transaction_type_new: str,
                            transaction_category: str, transaction_description: str, transaction_date: date):

        transaction = self.get_transaction_by_id(transaction_id)
        Transaction.validate(
            transaction_id,
            transaction_amount,
            transaction_type_new,
            transaction_category,
            transaction_description,
        )
        
        transaction.amount = transaction_amount
        transaction.type = transaction_type_new
        transaction.category = transaction_category
        transaction.description = transaction_description
        transaction.date = transaction_date

    def calculate_income(self):
        total_income = Decimal("0")

        for transaction in self.transactions:
            if transaction.type == "income":
                total_income += transaction.amount

        return total_income

    def calculate_expenses(self):
        total_expenses = Decimal("0")

        for transaction in self.transactions:
            if transaction.type == "expense":
                total_expenses += transaction.amount
        return total_expenses

    def calculate_balance(self):

        income = self.calculate_income()
        expenses = self.calculate_expenses()

        total_balance = income - expenses
        return total_balance

    def filter_by_description(self, description_keyword: str)-> list[Transaction]:

        results = []
        for transaction in self.transactions:
            if description_keyword.lower() in  transaction.description.lower():
                results.append(transaction)
        return results

    def filter_by_type(self, transaction_type: str)-> list:

        results = []
        for transaction in self.transactions:
            if transaction_type.lower() == transaction.type.lower() :
                results.append(transaction)
        return results

    def filter_by_category(self, category: str)-> list:
        results = []
        for transaction in self.transactions:
            if category.lower() == transaction.category.lower():
                results.append(transaction)
        return results

    def search_transactions(self, keyword: str) -> list[Transaction]:
        results = []

        for transaction in self.transactions:
            if (
                keyword.lower() in transaction.description.lower()
                or keyword.lower() in transaction.type.lower()
                or keyword.lower() in transaction.category.lower()
            ):
                results.append(transaction)

        return results


    def sort_transactions_asc(self):
        return sorted(
            self.transactions,
            key=lambda transaction: transaction.amount
        )

    def sort_transactions_dsc(self):
        return sorted(
            self.transactions,
            key=lambda transaction: transaction.amount,
            reverse = True
        )

    def sort_transactions_by_date_asc(self) -> list[Transaction]:
        return sorted(
            self.transactions,
            key=lambda transaction: transaction.date
        )

    def sort_transactions_by_date_dsc(self) -> list[Transaction]:
        return sorted(
            self.transactions,
            key=lambda transaction: transaction.date,
            reverse= True
        )
        
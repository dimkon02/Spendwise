from datetime import date
from decimal import Decimal

CATEGORIES = {
    "food",
    "housing",
    "transport",
    "entertainment",
    "shopping",
    "health",
    "bills",
    "salary",
    "other",
}

class Transaction:



    @staticmethod
    def validate( id: int, amount: Decimal, transaction_type: str, category: str, description: str, transaction_date: date):
        if id <= 0:
            raise ValueError("Invalid id")
        if amount<=0: 
            raise ValueError("Amount must be bigger than 0")
        if transaction_type not in ("income", "expense"): 
            raise ValueError( "Transaction type must be income or expense." )
        if not category.strip():
            raise ValueError("Category must not be empty")
        if category.lower() not in CATEGORIES:
            raise ValueError("Invalid category")
        if not description.strip():
            raise ValueError("Description cannot be empty.")
        if type(transaction_date) is not date:
            raise ValueError("Date must be a datetime.date (not a datetime or a string)")
        if transaction_date > date.today():
            raise ValueError("Date cannot be in the future")

    def __init__(self, id: int, amount: Decimal, transaction_type: str, category: str, description: str, transaction_date: date):
        self.validate(
            id,
            amount,
            transaction_type,
            category,
            description,
            transaction_date
        )
 
        self.id = id
        self.amount = amount
        self.type = transaction_type
        self.category = category
        self.description = description
        self.date = transaction_date

    def __str__(self):
        return f"{self.id} | {self.category} | {self.type} | {self.amount} | {self.description} | {self.date}"
    
from decimal import Decimal
from datetime import date
from models.transaction import CATEGORIES

def get_decimal(prompt: str) -> Decimal:
    while True:
        try:
            value = Decimal(input(prompt))
            if value > 0:
                return value
            
            print("Value must be positive")

        except ValueError:
            print("Invalid amount.")

def get_integer(prompt: str) -> int:
    while True:
        try:
            value = int(input(prompt))

            if value > 0:
                return value

            print("Invalid ID. Please enter a positive integer.")

        except ValueError:
            print("Invalid type. Please enter a whole number.")

def get_date(prompt: str) -> date:
    while True:
        try:
            value = date.fromisoformat(input(prompt).strip())
            return value
        except ValueError:
            print("Invalid date. Use YYYY-MM-DD.")

def get_non_empty_string(promt: str) -> str:
    while True:
        value = input(promt).strip()\

        if len(value) == 0:
            print("String cannot be empty.")
        else:
            return value

def get_transaction_type(prompt: str) -> str:
    while True:
        value = input(prompt).strip().lower()

        if value in ("income", "expense"):
            return value

        print("Invalid type. Please enter income or expense.")


def get_category(prompt: str) -> str:
    while True:
        value = input(prompt).strip().lower()

        if value in CATEGORIES:
            return value

        print("Invalid category.")
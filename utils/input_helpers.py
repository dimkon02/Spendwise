from decimal import Decimal, InvalidOperation
from datetime import date
from models.transaction import CATEGORIES

def get_decimal(prompt: str) -> Decimal:
    while True:
        try:
            value = Decimal(input(prompt))

            if not value.is_finite():
                print("Invalid amount.")
                continue

            if value > 0:
                return value

            print("Value must be positive")

        except InvalidOperation:
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
        raw = input(prompt).strip()
        
        if raw == "":
            return date.today()

        try:
            return date.fromisoformat(raw)
        except ValueError:
            print("Invalid date. Use YYYY-MM-DD.")

def get_non_empty_string(prompt: str) -> str:
    while True:
        value = input(prompt).strip()

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


def get_category(prompt: str, default: str | None = None) -> str:
    for number, category in enumerate(CATEGORIES, start=1):
        print(f"{number}. {category}")

    while True:
        value = input(prompt).strip()

        if value == "" and default is not None:
            return default

        if value.isdigit() and 1 <= int(value) <= len(CATEGORIES):
            return CATEGORIES[int(value) - 1]

        print(f"Invalid category. Enter a number from 1 to {len(CATEGORIES)}.")

from services.finance import FinanceManager
from models.transaction import Transaction
from services.storage import Storage
from utils.input_helpers import (
    get_decimal,
    get_integer,
    get_date,
    get_non_empty_string,
    get_transaction_type,
    get_category,
)

def get_transaction_data() -> tuple:
    transaction_id = get_integer("Transaction ID: ")
    transaction_amount = get_decimal("Transaction amount: ")
    transaction_type = get_transaction_type("Transaction Type: ")
    transaction_category = get_category("Transaction Category: ")
    transaction_description = get_non_empty_string("Transaction description: ")
    transaction_date =  get_date("Transaction date (YYYY-MM-DD): ")

    return (
        transaction_id, transaction_amount, transaction_type, transaction_category, transaction_description, transaction_date
    )

def add_transaction(
    manager: FinanceManager,
    storage: Storage,
) -> None:
    try:
        (
            transaction_id,
            transaction_amount,
            transaction_type,
            transaction_category,
            transaction_description,
            transaction_date,
        ) = get_transaction_data()

        transaction = Transaction(
            transaction_id,
            transaction_amount,
            transaction_type,
            transaction_category,
            transaction_description,
            transaction_date,
        )

        manager.add_transaction(transaction)
        storage.save_transactions(manager.get_transactions())

        print("Transaction added successfully.")

    except ValueError as error:
        print(f"Error: {error}")


def view_transactions(manager: FinanceManager) -> None:
    transactions = manager.get_transactions()

    if not transactions:
        print("No transactions found.")
    else:
        for transaction in transactions:
            print(transaction)

def search_transactions(manager: FinanceManager) -> None:
    print("1: Id")
    print("2: Type/Category/Description")

    input_choice_3 = input("What are you looking for? ")

    if input_choice_3 == "1":
        try:
            input_id = get_integer("Type id you are looking for: ")
            transaction_by_id = manager.get_transaction_by_id(input_id)
            print(transaction_by_id)
        except ValueError as error:
            print(f"Error: {error}")

    elif input_choice_3 == "2":
        input_search = input("What are you looking for? ")
        transaction_search = manager.search_transactions(input_search)

        if not transaction_search:
            print("No transactions found.")
        else:
            for transaction in transaction_search:
                print(transaction)

    else:
        print("Invalid search option.")

def filter_transactions(manager: FinanceManager) -> None:
    print("1. Type")
    print("2. Category")

    input_filter = input("Select filter option (1 or 2): ")

    if input_filter == "1":
        input_type = get_transaction_type("Select income or expense: ")
        transaction_by_type = manager.filter_by_type(input_type)

        if not transaction_by_type:
            print("No transactions found.")
        else:
            for transaction in transaction_by_type:
                print(transaction)

    elif input_filter == "2":
        input_category = get_category("Select category: ")
        transaction_by_category = manager.filter_by_category(input_category)

        if not transaction_by_category:
            print("No transactions found.")
        else:
            for transaction in transaction_by_category:
                print(transaction)

    else:
        print("Invalid filter option.")

def sort_transactions(manager: FinanceManager) -> None:
    print("1. Amount")
    print("2. Date")

    input_choice = input("Select what you want to sort by (1 or 2): ")

    if input_choice == "1":
        input_sort = input(
            "Select sorting order (asc or dsc): "
        ).strip().lower()

        if input_sort == "asc":
            transactions = manager.sort_transactions_asc()
        elif input_sort == "dsc":
            transactions = manager.sort_transactions_dsc()
        else:
            print("Invalid sorting option.")
            return

    elif input_choice == "2":
        input_sort = input(
            "Select sorting order (asc or dsc): "
        ).strip().lower()

        if input_sort == "asc":
            transactions = manager.sort_transactions_by_date_asc()
        elif input_sort == "dsc":
            transactions = manager.sort_transactions_by_date_dsc()
        else:
            print("Invalid sorting option.")
            return

    else:
        print("Invalid option.")
        return

    if not transactions:
        print("No transactions found.")
    else:
        for transaction in transactions:
            print(transaction)

def update_transaction(
    manager: FinanceManager,
    storage: Storage,
) -> None:
    try:
        (
            transaction_id,
            transaction_amount,
            transaction_type,
            transaction_category,
            transaction_description,
            transaction_date,
        ) = get_transaction_data()

        manager.update_transaction(
            transaction_id,
            transaction_amount,
            transaction_type,
            transaction_category,
            transaction_description,
            transaction_date,
        )

        storage.save_transactions(manager.get_transactions())

        print("Transaction updated successfully.")

    except ValueError as error:
        print(f"Error: {error}")

def delete_transaction(
    manager: FinanceManager,
    storage: Storage,
) -> None:
    input_id_delete = get_integer("Type id you want to delete: ")

    deleted = manager.delete_transaction(input_id_delete)

    if deleted:
        storage.save_transactions(manager.get_transactions())
        print("Transaction deleted successfully.")
    else:
        print("Transaction not found.")

def show_financial_summary(manager: FinanceManager) -> None:
    print("================================")
    print("           FINANCIAL SUMMARY")
    print("================================")

    total_income = manager.calculate_income()
    total_expense = manager.calculate_expenses()
    total_balance = manager.calculate_balance()

    print(f"Total income: {total_income}")
    print(f"Total expenses: {total_expense}")
    print(f"Total balance: {total_balance}")
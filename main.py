from services.finance import FinanceManager
from services.storage import Storage
from cli.transaction_menu import (
    add_transaction, 
    view_transactions, 
    search_transactions, 
    sort_transactions, 
    update_transaction, 
    delete_transaction, 
    show_financial_summary, 
    filter_transactions,
)


def main():

    
    storage = Storage("data/transactions.json")
    manager = FinanceManager()
    transactions = storage.load_transactions()

    for transaction in transactions:
        manager.add_transaction(transaction)


    while True:

        print("================================")
        print("           SPENDWISE")
        print("================================")
        print("1. Add Transaction")
        print("2. View Transactions")
        print("3. Search Transactions")
        print("4. Filter Transactions")
        print("5. Sort Transactions")
        print("6. Update Transaction")
        print("7. Delete Transaction")
        print("8. Financial Summary")
        print("9. Exit")
        print("================================")

        user_choice = input("Select your option: ")

        if user_choice == "1":
           add_transaction(manager, storage) 

        elif user_choice == "2":        
            view_transactions(manager)

        elif user_choice == "3":
            search_transactions(manager)

        elif user_choice == "4":
            filter_transactions(manager)

        elif user_choice == "5":
            sort_transactions(manager)
            
        elif user_choice == "6":
            update_transaction(manager, storage)

        elif user_choice == "7":
            delete_transaction(manager, storage)

        elif user_choice == "8":
            show_financial_summary(manager)

        elif user_choice == "9":
            print("Goodbye!")
            break
   
        else:
            print("Invalid choice. Please select 1-9.")


if __name__ == "__main__":
    main()
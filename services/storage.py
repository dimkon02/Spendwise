import json
from datetime import date
from decimal import Decimal
from pathlib import Path
from json import JSONDecodeError
from models.transaction import Transaction


class Storage:
    """
    Handle saving and loading SpendWise transactions to and from a JSON file.

    The Storage class is responsible only for persistence:
        Transaction objects -> JSON
        JSON -> Transaction objects
    """

    def __init__(self, file_path: str) -> None:
        """
        Create a Storage object.

        Args:
            file_path: Path to the JSON file used to store transactions.
        """
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

    def transaction_to_dict(self, transaction: Transaction) -> dict:
        """
        Convert a Transaction object into a dictionary.

        JSON cannot directly store custom Python objects such as
        Transaction, Decimal, or date. Therefore, we convert the
        transaction into basic Python data types first.

        Args:
            transaction: The Transaction object to convert.

        Returns:
            A dictionary containing the transaction data.
        """
        return {
            "id": transaction.id,
            "amount": str(transaction.amount),
            "type": transaction.type,
            "category": transaction.category,
            "description": transaction.description,
            "date": transaction.date.isoformat(),
        }

    def save_transactions(
        self,
        transactions: list[Transaction],
    ) -> None:
        """
        Save a list of Transaction objects to the JSON file.

        Each Transaction is converted into a dictionary before
        being written to the file.

        Args:
            transactions: List of transactions to save.
        """
        data = []

        for transaction in transactions:
            data.append(self.transaction_to_dict(transaction))

        with self.file_path.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    def dict_to_transaction(self, data: dict) -> Transaction:
        """
        Convert a dictionary back into a Transaction object.

        JSON stores all data using basic JSON-compatible types.
        Therefore:
            amount -> Decimal
            date   -> datetime.date

        Args:
            data: Dictionary containing transaction data.

        Returns:
            A reconstructed Transaction object.
        """
        return Transaction(
            data["id"],
            Decimal(data["amount"]),
            data["type"],
            data["category"],
            data["description"],
            date.fromisoformat(data["date"]),
        )

    def load_transactions(self) -> list[Transaction]:
        """
        Load transactions from the JSON file.

        The JSON data is first converted into Python dictionaries.
        Each dictionary is then converted into a Transaction object.

        Returns:
            A list of Transaction objects loaded from the file.
        """

        if self.file_path.exists():
            try:
                with self.file_path.open("r", encoding="utf-8") as file:
                    data = json.load(file)
            except JSONDecodeError:
                return []
        else:
            return []

        transactions = []

        for item in data:
            transactions.append(self.dict_to_transaction(item))

        return transactions
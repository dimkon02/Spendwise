from datetime import date
from decimal import Decimal

from models.transaction import Transaction
from services.storage import Storage


def create_transaction(
    transaction_id,
    amount,
    transaction_type,
    category,
    description,
    transaction_date,
):
    return Transaction(
        transaction_id,
        Decimal(amount),
        transaction_type,
        category,
        description,
        transaction_date,
    )


def test_save_and_load_transactions(tmp_path):
    file_path = tmp_path / "transactions.json"

    storage = Storage(str(file_path))

    transactions = [
        create_transaction(
            1,
            "50.00",
            "expense",
            "food",
            "Dinner",
            date(2026, 9, 3),
        )
    ]

    storage.save_transactions(transactions)

    loaded = storage.load_transactions()

    assert len(loaded) == 1
    assert loaded[0].id == 1
    assert loaded[0].amount == Decimal("50.00")
    assert loaded[0].type == "expense"
    assert loaded[0].category == "food"
    assert loaded[0].description == "Dinner"
    assert loaded[0].date == date(2026, 9, 3)


def test_save_multiple_transactions(tmp_path):
    file_path = tmp_path / "transactions.json"

    storage = Storage(str(file_path))

    transactions = [
        create_transaction(
            1,
            "50.00",
            "expense",
            "food",
            "Dinner",
            date(2026, 9, 1),
        ),
        create_transaction(
            2,
            "2500.00",
            "income",
            "salary",
            "Salary",
            date(2026, 9, 2),
        ),
    ]

    storage.save_transactions(transactions)

    loaded = storage.load_transactions()

    assert len(loaded) == 2


def test_missing_file_returns_empty_list(tmp_path):
    file_path = tmp_path / "transactions.json"

    storage = Storage(str(file_path))

    assert storage.load_transactions() == []


def test_creates_parent_directory(tmp_path):
    file_path = tmp_path / "data" / "transactions.json"

    storage = Storage(str(file_path))

    storage.save_transactions([])

    assert file_path.exists()


def test_empty_transaction_list(tmp_path):
    file_path = tmp_path / "transactions.json"

    storage = Storage(str(file_path))

    storage.save_transactions([])

    loaded = storage.load_transactions()

    assert loaded == []


def test_corrupt_json_returns_empty_list(tmp_path):
    file_path = tmp_path / "transactions.json"

    file_path.write_text(
        "this is not valid JSON",
        encoding="utf-8",
    )

    storage = Storage(str(file_path))

    assert storage.load_transactions() == []
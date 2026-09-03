from datetime import date
from decimal import Decimal

import pytest

from models.transaction import Transaction


def test_create_valid_transaction():
    transaction = Transaction(
        1,
        Decimal("50.00"),
        "expense",
        "food",
        "Dinner",
        date(2026, 9, 3),
    )

    assert transaction.id == 1
    assert transaction.amount == Decimal("50.00")
    assert transaction.type == "expense"
    assert transaction.category == "food"
    assert transaction.description == "Dinner"
    assert transaction.date == date(2026, 9, 3)


def test_invalid_id():
    with pytest.raises(ValueError):
        Transaction(
            0,
            Decimal("50.00"),
            "expense",
            "food",
            "Dinner",
            date(2026, 9, 3),
        )


def test_negative_id():
    with pytest.raises(ValueError):
        Transaction(
            -1,
            Decimal("50.00"),
            "expense",
            "food",
            "Dinner",
            date(2026, 9, 3),
        )


def test_zero_amount():
    with pytest.raises(ValueError):
        Transaction(
            1,
            Decimal("0"),
            "expense",
            "food",
            "Dinner",
            date(2026, 9, 3),
        )


def test_negative_amount():
    with pytest.raises(ValueError):
        Transaction(
            1,
            Decimal("-10.00"),
            "expense",
            "food",
            "Dinner",
            date(2026, 9, 3),
        )


def test_invalid_transaction_type():
    with pytest.raises(ValueError):
        Transaction(
            1,
            Decimal("50.00"),
            "banana",
            "food",
            "Dinner",
            date(2026, 9, 3),
        )


def test_invalid_category():
    with pytest.raises(ValueError):
        Transaction(
            1,
            Decimal("50.00"),
            "expense",
            "not_a_category",
            "Dinner",
            date(2026, 9, 3),
        )


def test_empty_description():
    with pytest.raises(ValueError):
        Transaction(
            1,
            Decimal("50.00"),
            "expense",
            "food",
            "",
            date(2026, 9, 3),
        )


def test_income_transaction():
    transaction = Transaction(
        2,
        Decimal("2500.00"),
        "income",
        "salary",
        "Monthly salary",
        date(2026, 9, 1),
    )

    assert transaction.type == "income"
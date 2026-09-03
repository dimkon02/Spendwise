from datetime import date
from decimal import Decimal

import pytest

from models.transaction import Transaction
from services.finance import FinanceManager


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


@pytest.fixture
def manager():
    return FinanceManager()


@pytest.fixture
def populated_manager(manager):
    transactions = [
        create_transaction(
            1,
            "100.00",
            "expense",
            "food",
            "Dinner",
            date(2026, 9, 1),
        ),
        create_transaction(
            2,
            "2000.00",
            "income",
            "salary",
            "Monthly salary",
            date(2026, 9, 2),
        ),
        create_transaction(
            3,
            "50.00",
            "expense",
            "transport",
            "Bus ticket",
            date(2026, 8, 30),
        ),
    ]

    for transaction in transactions:
        manager.add_transaction(transaction)

    return manager


# -------------------------
# ADD / GET
# -------------------------

def test_add_transaction(manager):
    transaction = create_transaction(
        1,
        "100.00",
        "expense",
        "food",
        "Dinner",
        date(2026, 9, 1),
    )

    manager.add_transaction(transaction)

    assert len(manager.get_transactions()) == 1
    assert manager.get_transaction_by_id(1) == transaction


def test_get_transaction_by_id(populated_manager):
    transaction = populated_manager.get_transaction_by_id(2)

    assert transaction.id == 2
    assert transaction.type == "income"


def test_get_nonexistent_transaction(populated_manager):
    with pytest.raises(ValueError, match="Transaction not found."):
        populated_manager.get_transaction_by_id(999)


def test_duplicate_transaction_id(manager):
    first = create_transaction(
        1,
        "100.00",
        "expense",
        "food",
        "Dinner",
        date(2026, 9, 1),
    )

    second = create_transaction(
        1,
        "200.00",
        "expense",
        "transport",
        "Bus",
        date(2026, 9, 2),
    )

    manager.add_transaction(first)

    with pytest.raises(ValueError, match="ID is already used."):
        manager.add_transaction(second)


# -------------------------
# UPDATE
# -------------------------

def test_update_transaction(populated_manager):
    populated_manager.update_transaction(
        1,
        Decimal("150.00"),
        "expense",
        "food",
        "Updated dinner",
        date(2026, 9, 3),
    )

    transaction = populated_manager.get_transaction_by_id(1)

    assert transaction.amount == Decimal("150.00")
    assert transaction.type == "expense"
    assert transaction.category == "food"
    assert transaction.description == "Updated dinner"
    assert transaction.date == date(2026, 9, 3)


def test_update_nonexistent_transaction(populated_manager):
    with pytest.raises(ValueError, match="Transaction not found."):
        populated_manager.update_transaction(
            999,
            Decimal("100.00"),
            "expense",
            "food",
            "Dinner",
            date(2026, 9, 3),
        )


# -------------------------
# DELETE
# -------------------------

def test_delete_transaction(populated_manager):
    deleted = populated_manager.delete_transaction(1)

    assert deleted is True

    with pytest.raises(ValueError, match="Transaction not found."):
        populated_manager.get_transaction_by_id(1)


def test_delete_nonexistent_transaction(populated_manager):
    deleted = populated_manager.delete_transaction(999)

    assert deleted is False


# -------------------------
# SEARCH
# -------------------------

def test_search_by_description(populated_manager):
    results = populated_manager.search_transactions("dinner")

    assert len(results) == 1
    assert results[0].id == 1


def test_search_by_category(populated_manager):
    results = populated_manager.search_transactions("salary")

    assert len(results) == 1
    assert results[0].id == 2


def test_search_by_type(populated_manager):
    results = populated_manager.search_transactions("expense")

    assert len(results) == 2


def test_search_case_insensitive(populated_manager):
    results = populated_manager.search_transactions("DINNER")

    assert len(results) == 1
    assert results[0].id == 1


def test_search_no_results(populated_manager):
    results = populated_manager.search_transactions("pizza")

    assert results == []


# -------------------------
# FILTER
# -------------------------

def test_filter_by_type(populated_manager):
    results = populated_manager.filter_by_type("expense")

    assert len(results) == 2
    assert all(
        transaction.type == "expense"
        for transaction in results
    )


def test_filter_by_category(populated_manager):
    results = populated_manager.filter_by_category("food")

    assert len(results) == 1
    assert results[0].id == 1


def test_filter_no_results(populated_manager):
    results = populated_manager.filter_by_category("shopping")

    assert results == []


# -------------------------
# SORT
# -------------------------

def test_sort_amount_ascending(populated_manager):
    results = populated_manager.sort_transactions_asc()

    amounts = [transaction.amount for transaction in results]

    assert amounts == [
        Decimal("50.00"),
        Decimal("100.00"),
        Decimal("2000.00"),
    ]


def test_sort_amount_descending(populated_manager):
    results = populated_manager.sort_transactions_dsc()

    amounts = [transaction.amount for transaction in results]

    assert amounts == [
        Decimal("2000.00"),
        Decimal("100.00"),
        Decimal("50.00"),
    ]


def test_sort_date_ascending(populated_manager):
    results = populated_manager.sort_transactions_by_date_asc()

    dates = [transaction.date for transaction in results]

    assert dates == [
        date(2026, 8, 30),
        date(2026, 9, 1),
        date(2026, 9, 2),
    ]


def test_sort_date_descending(populated_manager):
    results = populated_manager.sort_transactions_by_date_dsc()

    dates = [transaction.date for transaction in results]

    assert dates == [
        date(2026, 9, 2),
        date(2026, 9, 1),
        date(2026, 8, 30),
    ]


# -------------------------
# CALCULATIONS
# -------------------------

def test_calculate_income(populated_manager):
    assert populated_manager.calculate_income() == Decimal("2000.00")


def test_calculate_expenses(populated_manager):
    assert populated_manager.calculate_expenses() == Decimal("150.00")


def test_calculate_balance(populated_manager):
    assert populated_manager.calculate_balance() == Decimal("1850.00")


def test_empty_manager_calculations(manager):
    assert manager.calculate_income() == Decimal("0")
    assert manager.calculate_expenses() == Decimal("0")
    assert manager.calculate_balance() == Decimal("0")
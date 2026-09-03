# SPENDWISE

`Spendwise` is an application whose focus is managing personal finances, built enitrely in Python

The current project is the Command Line INterface (CLI) Beta, it focuses on Objecrt Oriented Programming, clean architecture,
validating data and automated testing.

## Functions:

- Add Transaction (id, amount, type, category, description, date)
- View Transactions
- Search Transactions, based on id, type, categoty or description
- Filter Transactions, based on type or category
- Sort Transactions, based on amount or date (ascending or descending order)
- Update Transaction
- Delete Transaction
- Caclulate Income, Expenses and Total Balance
- Save Transactions in JSON
- Handle missing and invalid JSON files
- Automated testing with pyest

# Project Structure

spendwise/
|- main.py
|- models/
|   |_______transaction.py
|- services
|   |________finance.py
|   |________storage.py
|- utils/
|    |_______input_helpers.py
|- cli/
|    |_______transaction_menu.py
|-test/
|     |_______test_finance.py
|     |_______test_storage.py
|     |_______test_transaction.py
|-data/
|- requiremnts.txt
|- .gitignore

##  Architecture

Spendwise delegates responsibilities in different layers

CLI -> FinanceManager -> Transaction Model

Storage -> JSON persistence

## Main Compentents

## Transaction:

Represents a financial transaction and is responsible for the validationo of data

## FinanceManager

Handles business logic including CRUD operations, searching, filtering, sorting, and financial calculations.

## Storage

Responsible for converting transactions to and from JSON and handling persistence.

## CLI

Handles user interaction and delegates operations to the appropriate application services.

## Technologies used

- Python
- pytest
- JSON
- OOP
- Git/GitHub

## Installation

Clone Repository:

git clone https://github.com/dimkon02/Spendwise.git 
cd Spendwise

Create/Activate Virtual Enviroment : 

puthon -m venv venv
.\venv\Scriprs\Activate.ps1

Install dependecies:

puthon -m pip install -r requirements.txt

## Running the Application

Run: 

python main.py

## Running tests

python -m pytest

## Current Status

SpendWise Python CLI Beta — Complete

The current release focuses on establishing a solid Python foundation before expanding the application into a full-stack web application.

## Future Development

Planned development includes:

- Django web application
- PostgreSQL database
- User authentication and user-specific transactions
- Web dashboard and visual analytics
- Docker containerization
- CI/CD with GitHub Actions
- AWS deployment
- Additional data analytics and machine learning capabilities

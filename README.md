# Demo REST API server

## Overview
This project is a Django REST Framework-based API server that provides paginated, sorted, and filtered endpoints for managing transactions and wallets. The API follows the JSON:API specification using `djangorestframework-jsonapi`. The project is built with the best modern tools and libraries, e.g. `uv` and `ruff`.

## Features
- **Wallet Management**: Create, update and retrieve wallets with balances automatically calculated from transactions.
- **Transaction Management**: Create and retrieve transactions linked to wallets with strict constraints to prevent negative balances.
- **Pagination, Sorting, and Filtering**: Implemented for both Wallet and Transaction models.
- **Strict Balance Constraint**: Ensures a wallet’s balance never goes negative.
- **Database Indexing**: Optimized queries with indexes where necessary.
- **Test Coverage**: Comprehensive tests (just for the `wallets` app, which is sufficient for demo purposes). ![Coverage](https://codecov.io/gh/pythonpro/api-demo/branch/main/graph/badge.svg)
- **Linting**: `ruff check` (run with `pre-commit` git hook).
- **Formatting**: `ruff format` and `isort` (run with `pre-commit` git hook).
- **Testing**: `pytest` tests (run with `pre-commit` git hook).

## Tech Stack
- **Python**: 3.13
- **Django**: 5.1
- **Django REST Framework**: 3.15
- **PostgreSQL**: 17
- **djangorestframework-jsonapi**: 7.1

## Installation & Setup

### Prerequisites
- Docker and docker compose

## Launching web server
```sh
docker compose up
```

## Running tests manually
```sh
docker compose run -it web bash -c 'DJANGO_SETTINGS_MODULE="config.settings" ./.venv/bin/pytest -s -v backend'
```
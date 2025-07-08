## Initial venv

```bash
python -m venv .venv
```

## Install Dependencies

```bash
python -m pip install -r requirements/base.txt
```

## Initialize the Database Migrations

```bash
python -m alembic revision --autogenerate -m "Initial migration"
```

## Run Database Migrations

```bash
python -m alembic upgrade head
```

## Run the Application

```bash
python -m uvicorn app.main:app --reload
```
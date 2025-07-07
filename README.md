## Install Dependencies

```bash
python3 -m pip install -r requirements/base.txt
```

## Initialize the Database Migrations

```bash
python3 -m alembic revision --autogenerate -m "Initial migration"
```

## Run Database Migrations

```bash
python3 -m alembic upgrade head
```

## Run the Application

```bash
python3 -m uvicorn app.main:app --reload
```
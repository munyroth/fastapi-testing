## Install Dependencies

```bash
python3 -m pip install -r requirements/base.txt
# or if you have pip installed globally
pip install -r requirements/base.txt
```

## Run the Application

```bash
python3 -m uvicorn app.main:app --reload
# or if you have uvicorn installed globally
uvicorn app.main:app --reload
```
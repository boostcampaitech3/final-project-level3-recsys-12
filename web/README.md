# LibraVerse(web)

A web implementation of LibraVerse using fastapi framework

## Requirements

- uvicorn, fastapi, pyyaml, sqlalchemy, psycopg2-binary, pydantic[email], passlib[bcrypt], python-jose[cryptography], Jinja2, python-multipart

## Usage
1. `pip install -r requirements.txt`
2. `python __main__.py`

## Configurations

```bash
├── db
│   ├── crud.py
│   ├── database.py
│   ├── load_data.py
│   ├── models.py
│   └── schemas.py
├── router
│   ├── books.py
│   ├── login.py
│   ├── logout.py
│   ├── mypage.py
│   ├── recsys.py
│   ├── register.py
│   ├── search.py
│   └── user_loan_info.py
├── static
├── templates
├── __main__.py
├── main.py
├── utils.py
└── requirements.txt
``` 

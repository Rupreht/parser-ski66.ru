# parser for site ski66.ru

Sports event parser

## Launching ;-)

```sh
pip install -U setuptools pip
pip install -r requirements.txt
mkdir data
```

```sh
echo TOKEN_BOT=.... >> .env
```

## Flask

```sh
flask shell
from app import db, create_app, models
db.create_all(app=create_app())
```

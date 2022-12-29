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
echo USER_LOGIN=.... >> .env
echo USER_NAME=.... >> .env
echo USER_PASSWD=.... >> .env
```

## Flask

```sh
flask shell
```

```python
from os import getenv
from app import db, create_app, models
from werkzeug.security import generate_password_hash
db.create_all(app=create_app())

new_user = models.User(email=getenv("USER_LOGIN"), username=getenv("USER_NAME"),
    password=generate_password_hash(getenv("USER_PASSWD"), method='sha256'))
db.session.add(new_user)
db.session.commit()
```

## uWSGI

```sh
uwsgi --http 0.0.0.0:80 --wsgi-file app/main.py --callable app --stats 0.0.0.0:81
```

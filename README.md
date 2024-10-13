# Project Setup and Access Guide

This guide will walk you through setting up the project locally .Please follow these steps carefully for a smooth setup.

## Local Setup

1. Clone the project repository to your local machine.
2. Go inside playlist/project folder
```
bash

cd playlist

python -m venv .venv

source .venv/bin/activate
pip install -r requirements.txt

cd project
python manage.py runserver
```
4. migrate:
```
bash

python manage.py migrate
```
5. check migration status
```
bash

python manage.py showmigrations
```
6. Populate songs
```
bash

(open interactive shell)
python manage.py shell

from songs.utils import *
songs_populator()

```

7. create superuser (optional)
- To access admin
http://localhost:8000/admin/
```
bash
python manage.py createsuperuser
```


### Postman collection

- under playlist folder

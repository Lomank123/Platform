# Platform


Unified User Platform - Service which provides authentication to other products.


## Prerequisites

- Python 3.11+
- Docker


## Installation

- Create `.env` file and copy the content of `.env.example` to it (don't forget to change env variables):

```shell
touch .env
cp .env.example .env
```

- Create `venv`:

```shell
mkdir venv
cd venv
python -m venv .
cd ..
source venv/bin/activate
```

- Install requirements:

```shell
pip install -r requirements.txt
```

- Build and start Docker containers:

```shell
docker compose up -d --build
```


## Utilities

- Create superuser:

```shell
docker compose exec platform python manage.py createsuperuser --noinput
```

Note: Check superuser credentials in `.env` file.


- To clear all blacklisted refresh tokens which have expired:

```shell
docker compose exec platform python manage.py flushexpiredtokens
```


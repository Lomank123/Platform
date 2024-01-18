# Platform


Unified User Platform - Service which provides authentication to other products.


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

- Run migrations:

```shell
python manage.py migrate
```

- Start the server:

```shell
python manage.py runserver
```

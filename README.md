# Nora the Cooker

This is a distribution food system for its administration.

---

## Development Backend Installation

---

You’ll start the project with this minimum dependencies.

- virtualenv 16.6.0
- Python 3.6.7
- pip 19.1.1
- PostgreSQL 10.8 (You can use any else)
- celery 3.1.18
- Redis Server 3.2.9

Don't forget fill the env file ;)

After that, you need to create the enviroments and activate it, then you run the next commands:

```sh
>> sudo apt-get install redis-server
>> sudo systemctl enable redis-server.service
>> pip install -r requirements.txt
>> python manage.py migrate
>> python manage.py createsuperuser
>> celery -A config worker -l info
>> celery -A deliveries worker -l info
>> python manage.py runserver
```

---

## Docker

### Creation the first user

```sh
docker exec -it <container_id> python3 manage.py createsuperuser
```

### Run the container

```sh
docker-compose up --force-recreate -d
```

---

## Model

to be continue...

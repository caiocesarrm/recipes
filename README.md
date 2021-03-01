# Apicbase assignment

This project presents a platform to manage recipes and ingredients.
On the architectural side, the project is almost production ready, with enviroments and celery inplace ready to run.

## How to run

Install [docker](https://get.docker.com/) and docker-compose.

to run only django (RECOMMENDED):
```bash
docker-compose up
```
to run django with celery, rabbitmq and flower:
```bash
docker-compose -f docker-compose-dev.yml up --build
```

access: http://localhost:5000/

## Erasing/modifying the database

migrations are already applied, if you want a clean database, delete db.abrecipes.sqlite3

then get the container id with:
```bash
docker ps -q
```
example:

then run the following command with the container id to enter inside the container
```bash
docker exec -it af092b1443bf bash
```
inside the container you can run:
```bash
python3 manage.py makemigrations
python3 manage.py migrate
```
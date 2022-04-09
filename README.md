# Movie API
A Movie Database API built with Django, Django REST framework, PostgreSQL and Docker

## Getting Started

#### Requirements:

- docker
- docker-compose

#### Startup:
```bash
docker-compose up -d --build
```

#### Make migrations:
```bash
docker-compose exec web python /code/app/manage.py makemigrations
docker-compose exec web python /code/app/manage.py migrate
```

#### Create superuser
```bash
docker-compose exec web python /code/app/manage.py createsuperuser
```

#### Populate DB
Exec:
```commandline
docker-compose exec web python /code/app/manage.py populate_db --path=/code/data/genres.csv --app_name=core --model_name=Genre
docker-compose exec web python /code/app/manage.py populate_db --path=/code/data/movies.csv --app_name=core --model_name=Movie
docker-compose exec web python /code/app/manage.py populate_db --path=/code/data/networks.csv --app_name=core --model_name=Network
```

#### Execute tests
```shell
./tests-run.sh
```

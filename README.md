# Mastermind Api using DDD and Event Sourcing

This project is a refactor of the [Mastermind API](https://gitlab.com/Alcasser/mastermind-api) 
I made some months ago using Django + Django Rest Framework.
I'm using an experimental DDD approach with Event Sourcing (based on [this project](https://github.com/Hyaxia/Bank-DDD-CQRS-ES/tree/master/bank_ddd_es_cqrs/accounts))
found in [this repo](https://github.com/valignatev/ddd-dynamic).

The api is currently using Postgres as an event store. You can store game aggregates which are related to a
series of generated Domain Events. Loading a game current state is the left fold of those events.

The business logic is decoupled from the infrastructure used. This means we could easily move from
Flask to another framework without touching the business code or inject another implementation of the
WriteRepository to use a different storage mechanism.


## Requirements

* Install the Docker tools on [Mac](https://docs.docker.com/docker-for-mac/) or [Windows](https://docs.docker.com/docker-for-windows/).

## Setup instructions

*  `git clone && cd` the repository.

In order to develop using the local environment:

*  `docker-compose build` will build the Flask Api image. Postgres uses an image.
*  `docker-compose up -d` will create the containers.
*  `docker logs -f mastermind-flask-api --tail 10` to view the api logs.
*  `docker exec -it mastermind-flask-api python manage.py create_games_db` needs to be used to create the database.
*  `docker exec -it mastermind-flask-api pytest -s` can be used to run the tests


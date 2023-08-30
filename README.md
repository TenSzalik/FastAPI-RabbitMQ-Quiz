# Philosophical Compass

A RESTFul site that allows you to create quizzes, give answers, and create a radar chart by answer. The project is primarily oriented towards measuring philosophical views, but it can be used for something else.

The main goal of this project is to gain an in-depth understanding of web development, a better understanding of FastAPI, OOP, RabbitMQ and some fun =)

*Thanks to Joanna Płatek for preparing the background and icon of Marcus Aurelius. She can be followed [here](https://www.instagram.com/petlart/)*.

## Table of content

- [Tech stack](#tech-stack)
    - [Backend](#backend)
    - [Frontend](#frontend)
- [How it works](#how-it-works)
    - [Technical overview](#technical-overview)
    - [Flow chart](#flow-chart)
    - [Home page](#home-page)
    - [Start quiz](#start-quiz)
    - [Endpoints](#endpoints)
- [Fast way to run](#fast-way-to-run-on-linux)
    - [Backend](#backend-1)
    - [Frontend](#frontend-1)
- [Developing](#developing)
    - [Creating your own quiz](#creating-your-own-quiz)
    - [Testing](#debugger)
    - [Debugger](#debugger)
    - [Useful commands](#useful-commands)
- [Technical details](#technical-details)
    - [Tree](#tree)

## Tech stack

### Backend

- Python3 
- FastAPI (backend framework)
    - Pydantic (data validation)
    - uvicorn (asgi web server)
- RabbitMQ (message broker)
    - pika (pure-Python implementation of the AMQP 0-9-1)
- PostgreSQL (database)
    - SQLAlchemy (ORM)
    - Alembic (migration tool)
    - psycopg2 (database adapter for python)
- Pytest (testing)
    - httpx (http client for testing)
- Docker (container)
    - docker compose (local development)
- Pylint (linter, [settings are here](backend/.pylintrc))
- Black (code formatter)
- JWT (security)
    - python-jose (coding and decoding JWT)
    - passlib (hashing password)

Specyfic versions you can see in [requirements](backend/requirements.txt) and [requirements_dev](backend/requirements_dev.txt)

### Frontend

- JavaScript/TypeScript
    - Plotly (chart generating tool)
    - React (library for JS)
        - react-router-dom (routing)
- HTML
- CSS
    - Tailwind (library for CSS)
- Vite (development environment)

## How it works

### Technical overview

When we start the test, RabbitMQ creates a queue for us that collects all the answers to the questions. The name of the queue is generated using UUID4 and stored in a cookie. At the end of the test, we return all the data from the queue, analyze it using the Plotly library and return it in the form of a radar chart. The answers are stored in the database, which will allow for statistical analysis in the future. Creating your own quiz requires creating a user and logging in with a JWT token.

If you are interested in how it works see [Technical details](#technical-details)

### Flowchart

![img](https://i.imgur.com/fUW3se0.jpg)

### Home page

![img](https://i.imgur.com/uAk1zRA.png)

### Starting the quiz

![img](https://i.imgur.com/lzKrq3f.png)

### Endpoints

![img](https://i.imgur.com/qKoMbzj.png)

## Fast way to run (on Linux)

### Backend

Go to [/backend](/backend) and run:

`docker compose up --build`

More: [running app](backend/docs/running.md)

### Frontend

The frontend is handled by Vite. First install npm and Vite globally:

`sudo apt install nodejs npm`

`npm install -g vite`

Go to the [frontend](/frontend) and run:

`npm install`

`npm run dev`

## Developing

- Swagger: http://localhost:8000/docs

- Pgadmin: http://localhost:5050/

- RabbitMQ: http://localhost:15672/

### Creating your own quiz

If you want to create your own quiz, you need to create a user and then authorize it at the JWT endpoint. You need a secret key to create the user - you can find it in the [.env](backend/.env) file. Now you can send data to the endpoints!

### Testing

1. Check the active containers (for the name):

    `docker ps`

2. Run (web service, container must be active):

    `docker exec -it <container_name> pytest tests/tests_*.py`


### Debugger

If you want to run pdb/breakpoint on a running server, you need to open the console and run:

`docker attach <container_name>`.

In this console, you will operate the debugger. You can see these lines inside docker-compose.yml:

```
stdin_open: true
tty: true
```

It's responsible for allowing the debugger to run inside the docker container.

### Useful commands

`docker exec -it <container_name> pylint --recursive=y core conftest.py main.py`

`docker exec -it <container_name> black .`

## Technical details

RabbitMQ is one of the most popular open source message brokers. It supports multiple messaging protocols and streaming. Compass is used with AMQP, whose schema looks as follows:

![img](https://assets.website-files.com/5ff66329429d880392f6cba2/619f53ce469a19d18a61ef94_AMQP%20Broker.png)

All communication with RabbitMQ is done through endpoints. Generally, RESTful style excludes endpoint names such as "delete" "create", but in our case the methods in the endpoints don't matter - we use the POST method everywhere and don't work on the database, but always send data to the RabbitMQ server

In our case, the user is the publisher, sends the answers to the queue through the exchange, and when the quiz is completed, the queue is consumed by the endpoint and sent to plotly, which generates a graph based on the answers.

Using the AMQP protocol gives us a lot of potential. It is a different server, so everything is very stable, we can go back to the quiz after a long time on the same question and so on.

Generally, the answer sent to the queue looks like the following:

```json
{
  "queue": "string",
  "category": "string",
  "answer": 0
}
```

But this answer when consumed turns into this:

```json
{ "category": 0} # category name and points
```

Then, when you have several such JSONs, the function transforms them, summing them, into something more consumable by plotly:

from:

```json
{ "empiricism": 2}
{ "empiricism": -1}
{ "rationalism": 0}
{ "rationalism": 2}
{ "naturalism": -2}
{ "naturalism": -2}
{ "anti-naturalism": 2}
{ "anti-naturalism": 2}
```
to:

```json
{
    "empiricism": 1,
    "rationalism": 2,
    "naturalism": -4,
    "anti-naturalism": 4
}
```

and based on this plotly can generate a radar chart for us. The last of the JSON is written to the PostgreSQL database with the user's age and gender - it is generated from the browser and looks as follows:

```json
{ "age": 24, "sex": "male", "quiz": "{"category": 11}"}
```

The frontend is mainly based on React components and Tailwind styles. Using Compass is easy for the client. The customer just needs to click "Ready to play with us?" and provide an answer and that's it.

### Tree

```bash
.
├── alembic
│   ├── env.py
│   ├── README
│   ├── script.py.mako
│   └── versions # versions of migrations
│       └── 8df6346c48a3_second_revision.py
├── alembic.ini # db configuration
├── conftest.py # fixtures for testing
├── core
│   ├── endpoints # all endpoints
│   │   ├── __init__.py
│   │   ├── queue.py
│   │   ├── quiz.py
│   │   ├── token.py
│   │   └── user.py
│   ├── managers
│   │   ├── __init__.py
│   │   └── rabbit_manager.py # connection with RabbitMQ server
│   ├── models
│   │   ├── __init__.py
│   │   ├── database.py # connecting to the db
│   │   ├── models.py # SQLAlchemy models
│   │   └── schemas.py # Pydantic schemas/models
│   └── utils # some useful functions
│       ├── get_hashed_password.py
│       ├── get_sum_dicts.py
│       ├── load_simple_db.py
│       └── verify_password.py
├── docker-compose.yml
├── Dockerfile
├── .env # all credentials in enviroment are here
├── main.py
├── requirements_dev.txt
├── requirements.txt
├── .pylintrc # pylint settings
└── tests
    ├── tests_quiz.py
    ├── tests_rabbit.py
    ├── tests_token.py
    └── tests_user.py
```

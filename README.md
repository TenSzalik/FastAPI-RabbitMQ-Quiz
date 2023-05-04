# Philosophical Compass

Short description: When we start the test, RabbitMQ creates a queue for us that collects all the answers to the questions. The name of the queue is generated using UUID4 and stored in a cookie. At the end of the test, we return all the data from the queue, analyze it using the Plotly library and return it in the form of a radar chart. The responses are saved to a database which will allow for a statistical analysis in the future.

At this point, the project has a fully functional backend and frontend.

## Flow chart

![img](https://i.imgur.com/pQa7Byo.jpg)

## Gif

![gif](https://i.imgur.com/X06UsW9.gif)

## Tech stack

- FastAPI
- RabbitMQ
- SQLAlchemy
- Alembic
- Plotly
- PostgreSQL
- JavaScript/TypeScript
- React
- Vite
- Tailwind

## How to run (on Linux)

### Backend

1. Install docker locally and download the container from RabbitMQ:

    > sudo docker run --hostname localhost --name rabbit-server -e RABBITMQ_DEFAULT_USER=guest -e RABBITMQ_DEFAULT_PASS=guest1234 -p 5672:5672 -p 15672:15672 rabbitmq:3-management

    if the container does not start:

    > sudo docker start rabbit-server

2. Install PostgreSQL, create db and set username and password in `backend/core/models/database`

3. Create virtual enviroment for Python:

    > python3 -m venv venv

    > source venv/bin/activate

4. Install requirements included in file requirements.txt

    > pip install -r requirements.txt

5. After instalation complete you can run server with project

    > uvicorn main:app --host localhost --port 4000 --reload

6. Sending data for endpoints /quiz requires migration

    > alembic upgrade head

    > alembic revision --autogenerate -m "First revision" 

    > alembic upgrade head

### Frontend

The frontend is handled by Vite. First install npm and Vite globally:

> sudo apt install nodejs npm

> npm install -g vite

Go to the `/frontend` and run:

> npm install

> npm install react-router-dom@6

> npm run dev

The port should be set to 5173. This is required by the backend, otherwise you will get a CORS error. You can change the available ports in `backend/main.py`
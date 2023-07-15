Running `docker compose --build` creates 4 containers:

1. web
    - FastAPI backend
2. db
    - PostgreSQL database
3. db-test
    - another PostgreSQL database generated for testing
4. pgadmin
    - PostgreSQL GUI

The web container is run from this command:

`python3 main.py`

You can see how it works in [main.py](../main.py):

```python
DEBUG = True

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

    if DEBUG is True:
        alembic_cfg = Config("alembic.ini")
        command.upgrade(alembic_cfg, "head")
        load_simple_db(SessionLocal())
```

As you can see, the hostname and port are hard-coded and can be changed at will. One thing here is tricky:

`"main:app"`

You can successfully change it to `app` (as the fastapi docs recommend), but your debugger in docker will not work.

In theory, there is no need to create the `DEBUG` variable and you can replace it with `__debug__` and run the backend only in optimized mode (`python -o`) to change `__debug__` to false. It would look like this:

```python
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

    if __debug__ is True:
        alembic_cfg = Config("alembic.ini")
        command.upgrade(alembic_cfg, "head")
        load_simple_db(SessionLocal())
```

and run it in docker-compose.yml:

`python3 -o main.py`

But I haven't tested it. Also, you will lose all assertions, so testing is impossible.

The following lines are responsible for:

1. loading migration from alembic [version](../alembic/versions/) to the PostgreSQL database

2. loading a simple database for testing and quick overview

By default you get the actual migration in [version](../alembic/versions/), so you don't need to create your own. If you want, you can run:

```bash
docker compose run web alembic upgrade head

docker compose run web alembic revision --autogenerate -m "First revision"

docker compose run web alembic upgrade head
```

**Important:** create the migration *required* "versions" folder inside the "alembic" folder.

Next: instead of loading "simple database" you can simply:

1. send data to endpoint [(look here for more)](../../README.md#creating-your-own-quiz)

2. log into pgadmin (PostgreSQL GUI) hosted by docker and create the quiz via SQL
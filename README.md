# Video Storage 🎥

This is an implementation of imaginary `video-storage.com` service based on [requirements](etc/task.pdf) and OpenAPI [schema](etc/openapi.yml).

I supposed enough flexibility to extend/change the schema/requirements for the sake of making better design decisions.
For example - delete video operation will return object being deleted instead of no content. There are multiple details like this one.

Some important notes:

- Initial accounts/credentials are created so that system could be easily tested, you will need them and can find them all in [.env](.env) file.
- You can download extended/modified OpenAPI schema from the running API and Swagger UI (link below)
- Videos are stored on the server, but in the real world scenario they would be on shared distributed file/object storage like AWS EFS/S3, for example.
- As an additional task, I opted out for auth and user management, you will notice that initial video requirement and endpoints are not secured, so that they could be tested independently of auth/user management. Additional `/items` endpoint is provided to test auth/user feature. In the real world scenario auth/user management and video storage would be separated services.
- Everything is covered with tests, but as always - potential improvement could be to increase test coverage.
- Email functionality won't work until you add credentials in `.env` file.
- Two video files are provided for testing purposes under [etc](etc) folder.
- I did nice configuration with Traefik proxy, so that's why I didn't want to mess up with `restapi-challenge-nework` requirement to block the internet, but I just want to show that it would be easy to do it in Docker Compose: 1) name the network as requested and 2) configure the nework with `internal: true`
- So, there are 3 main components:
    - Backend - Video Storage
    - Backend - Auth & User Management
    - CLI

## Requirements

The latest:

* [Docker / Compose](https://www.docker.com)
* [Python](https://www.python.org)
* [Poetry](https://python-poetry.org) for Python package and environment management

## Backend

Start the stack with Docker Compose:

```bash
docker-compose up
```

**Note**: The first time you start your stack, it might take a minute for it to be ready. While the backend waits for the database to be ready and configures everything.

Now you can open your browser and interact with these URLs:

- Automatic interactive documentation with Swagger UI: http://localhost/docs
- OpenAPI Schema: http://localhost/api/v1/openapi.json
- Backend based on [FastAPI](https://fastapi.tiangolo.com/) Python framework: http://localhost/api
- [PGAdmin](https://www.pgadmin.org), PostgreSQL Web administration: http://localhost:5050
- [Flower](https://github.com/mher/flower), administration of Celery tasks: http://localhost:5555
- [Traefik](https://traefik.io) UI, to see how the routes are being handled by the proxy: http://localhost:8090

At this point you can already use backend API with provided Swagger UI or with your favorite tool.

If you want to develop, you will find instruction below.

By default, the dependencies are managed with [Poetry](https://python-poetry.org/), go there and install it.

From `./backend/app/` you can install all the dependencies with:

```console
$ poetry install
```

In case you get an error regarding Postgres tools, you might need to install them, the easiest way on Mac:

```console
$ brew install postgresql
```

Then you can start a shell session with the new environment with:

```console
$ poetry shell
```

Next, open your editor at `./backend/app/` (instead of the project root: `./`), so that you see an `./app/` directory with your code inside. That way, your editor will be able to find all the imports, etc. Make sure your editor uses the environment you just created with Poetry.

Modify or add SQLAlchemy models in `./backend/app/app/models/`, Pydantic schemas in `./backend/app/app/schemas/`, API endpoints in `./backend/app/app/api/`, CRUD (Create, Read, Update, Delete) utils in `./backend/app/app/crud/`. The easiest might be to copy the ones for Items (models, endpoints, and CRUD utils) and update them to your needs.

Add and modify tasks to the Celery worker in `./backend/app/app/worker.py`.

If you need to install any additional package to the worker, add it to the file `./backend/app/celeryworker.dockerfile`.

During development, you can change Docker Compose settings that will only affect the local development environment, in the file `docker-compose.override.yml`.

The changes to that file only affect the local development environment, not the production environment. So, you can add "temporary" changes that help the development workflow.

The directory with the backend code is mounted as a Docker "host volume", mapping the code you change live to the directory inside the container. That allows you to test your changes right away, without having to build the Docker image again. It should only be done during development, for production, you should build the Docker image with a recent version of the backend code. But during development, it allows you to iterate very fast.

You can enter inside the running container:

```console
$ docker-compose exec backend bash
```

You should see an output like:

```console
root@7f2607af31c3:/app#
```

That means that you are in a `bash` session inside your container, as a `root` user, under the `/app` directory.

As during local development your app directory is mounted as a volume inside the container, you can also run the migrations with `alembic` commands inside the container and the migration code will be in your app directory (instead of being only inside the container). So you can add it to your git repository.

Make sure you create a "revision" of your models and that you "upgrade" your database with that revision every time you change them. As this is what will update the tables in your database. Otherwise, your application will have errors.

Start an interactive session in the backend container:

```console
$ docker-compose exec backend bash
```

If you created a new model in `./backend/app/app/models/`, make sure to import it in `./backend/app/app/db/base.py`, that Python module (`base.py`) that imports all the models will be used by Alembic.

After changing a model (for example, adding a column), inside the container, create a revision, e.g.:

```console
$ alembic revision --autogenerate -m "Add column last_name to User model"
```

Commit to the git repository the files generated in the alembic directory.

After creating the revision, run the migration in the database (this is what will actually change the database):

```console
$ alembic upgrade head
```

If you don't want to use migrations at all, uncomment the line in the file at `./backend/app/app/db/init_db.py` with:

```python
Base.metadata.create_all(bind=engine)
```

and comment the line in the file `prestart.sh` that contains:

```console
$ alembic upgrade head
```

If you don't want to start with the default models and want to remove them / modify them, from the beginning, without having any previous revision, you can remove the revision files (`.py` Python files) under `./backend/app/alembic/versions/`. And then create a first migration as described above.

To test the backend run:

```Bash
DOMAIN=backend sh ./scripts/test-local.sh
```

**Note:** This will stop currently running stack to start the new one for testing purposes.

## CLI

See [CLI](cli).
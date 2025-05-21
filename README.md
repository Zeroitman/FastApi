# FastAPI Backend

**[FastAPI-Project](https://github.com/Zeroitman/FastApi)**

Demonstration FastAPI project. 

The service uses the following technologies:

- `Python 3.10`
- `FastApi 0.115`
- `PostreSQL 13.3`
- `Docker`
- `Poetry`

## Local Development

In order to deploy the project for local development, one should:
 1. clone from the remote repository 
 2. copy default envs (and change them if there is a need)
 3. execute docker-compose command (make sure that you have docker and docker-compose installed on your machine)
```
cd {project_folder}
cp .env.sample .env
docker-compose up
```

### Migrate 
In order to generate migrations for different modules, one should
- add the path to new migrations set in *version_locations* at alembic.ini
- create initial migration
```bash
$ poetry run alembic revision --autogenerate --branch-label={module name} --version-path={path_to_module_migrations} --head=base -m 'initial'
```
In order to add migration to existing migrations module, one should
```bash
$ poetry run alembic revision --autogenerate -m '{name of migration}' --head={module name}@head
```
In order to add migration that depends on other migration (depends, not follows), one should
```bash
$ poetry run alembic revision --autogenerate -m '{name of migration}' --head={module name}@head --depends-on={migration ID or other module name}
```
Run + 1 migration on module
```bash
$ poetry run alembic upgrade {module name}@+1
```
Run -1 migration on module  
```bash
$ poetry run alembic downgrade {module name}@-1
```
Run all migrations at all modules ahead
```bash
$ poetry run alembic upgrade heads
```

### How to run tests
Tests are run either from virtual environment or from docker container by following commands:
```bash
$ poetry run pytest # Run all tests
$ poetry run pytest --cov=user_backend # Run tests with coverage
$ poetry run pytest --cov=user_backend/ --cov-report=html # Run tests wtith coverage into local html file
$ poetry run pytest -k TestEditProfileView # Run specific testcase
$ poetry run pytest -k test_edit_profile_success # Run specific test
```


## List of environment variables
| Key                          | Description                                                                                                                                  | Default value               |
|:-----------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------|:----------------------------|
| POSTGRES_USER                | database user                                                                                                                                | postgres                    |
| POSTGRES_PASSWORD            | database password                                                                                                                            | postgres                    |
| DATABASE_NAME                | database name                                                                                                                                | fa_db                       |
| POSTGRES_HOST                | database host, for containers - name of container                                                                                            | fa-db                       |
| POSTGRES_PORT                | database port                                                                                                                                | 5432                        |
| CONNECTION_POOL              | the maximum primary number of connections that will be opened and supported by the pool                                                      | 5                           |
| MAX_OVERFLOW                 | how many additional connections can be created beyond connection_pool if all are busy                                                        | 10                          |
| POOL_RECYCLE                 | after how many seconds the connection will be automatically closed and recreated                                                             | 3600                        |
| DRF_CONN                     | parameters for microservices to communication. Passed as a single string value, then parsed into multiple parts using &#124; as a separator  | "key&#124;message&#124;url" |
| SECRET_KEY                   | secret string that the server uses to sign the JWT                                                                                           | a94f6b2d7e183c5a9c12e847d9  |
| ACCESS_TOKEN_EXPIRE_MINUTES  | access token expiration date                                                                                                                 | 30                          |
| REFRESH_TOKEN_EXPIRE_MINUTES | refresh token expiration date                                                                                                                | 1440                        |
 

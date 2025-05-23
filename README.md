# FastAPI Backend

# About the project (EN)
Demonstration FastAPI project that implements
1. Automatic project startup with all services with 3 commands:
   - `cd {project_folder}` — go to the project folder
   - `cp .env.sample .env` — copy environment variables
   - `docker-compose up` — run a multi-container application
2. Automatic documentation of API methods in OpenAPI 3.0 format
3. Method for user registration with validations
4. Authentication via JWT with methods for obtaining access_token and refresh_token
5. Method for obtaining full user information
5. Method for updating user information
6. Method for deleting a user
7. Method for obtaining a list of active banners from another service **[DRF-Project](https://github.com/Zeroitman/DRF)** with pagination and checking rights to communicate microservices
8. All functionality is covered tests

# О проекте (RU)
Демонстрационный FastAPI проект в котором реализовано 
1. Автоматическое поднятие проекта со всеми сервисами 3 командами:
   - `cd {project_folder}` — зайдите в папку проекта
   - `cp .env.sample .env` — скопируйте переменные окружения
   - `docker-compose up` — запустите мультиконтейнерное приложение
2. Автоматическая документация АПИ методов в формате OpenAPI 3.0
3. Метод для регистрации пользователя с валидациями
4. Аутентификации через JWT с методами для получения access_token и refresh_token
5. Метод для получения полной информации о пользователе
6. Метод для обновления информации о пользователе
7. Метод для удаления пользователя
8. Метод для получения списка действующих баннеров с другого сервиса **[DRF-Project](https://github.com/Zeroitman/DRF)** с пагинацией и проверкой прав на коммуникацию микросервисов
9. Весь функционал покрыт тестами

# The service uses the following technologies:

- `Python 3.10`
- `FastApi 0.115`
- `PostreSQL 13.3`
- `Docker`
- `Poetry`
- `Redis`
- `Pytest`

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

## How to run tests

When docker container is running, one must enter container
```
docker exec -it fast-api-project bash
```
and execute the command for testing
```
pytest
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
| REDIS_HOST                   | redis server address, for containers - name of container                                                                                     | fa-redis                    |
| REDIS_PORT                   | redis port                                                                                                                                   | 6379                        |
| REDIS_DB                     | redis logical base number                                                                                                                    | 0                           |
 

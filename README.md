### Setup

```shell
kubectl create ns fastapi
kubectl apply -n fastapi -f k8s
kubectl exec -it -n fastapi deploy/fastapi -- zsh
```

### Database Migration

```shell
alembic init alembic
sed -i '1i\from app.config import settings\nfrom app.database import Base\n' alembic/env.py
sed -i 's|target_metadata = None|target_metadata = Base.metadata|g' alembic/env.py
sed -i '19i\config.set_main_option("sqlalchemy.url", settings.db_url)' alembic/env.py
isort alembic && black alembic
alembic revision --autogenerate -m "Init: Migration"
```

### FastAPI

```shell
uvicorn app.main:app --host 0.0.0.0
```

### Client

```shell
python client/main.py
```

### Logs

```python
[07/11/24 15:31:19] INFO     [FastAPI] [database] get_postgres: Connect                                                                       database.py:21
                    INFO     [FastAPI] [routers/accounts] create_account: Checking Zerohertz was created...                                   accounts.py:18
                    DEBUG    [FastAPI] [crud] get_account_by_username: Zerohertz                                                                  crud.py:23
                    DEBUG    [FastAPI] [crud] _fetch_by_id: <class 'app.models.Account'>                                                          crud.py:28
[07/11/24 15:31:20] INFO     [FastAPI] [routers/accounts] create_account: Zerohertz was already created                                       accounts.py:23
                    INFO     [FastAPI] [database] get_postgres: Close                                                                         database.py:27
INFO:     {IP}.{IP}.{IP}.{IP}:62485 - "POST /accounts/ HTTP/1.1" 200 OK
                    INFO     [FastAPI] [database] get_postgres: Connect                                                                       database.py:21
                    INFO     [FastAPI] [database] get_redis: Connect                                                                          database.py:31
                    INFO     [FastAPI] [routers/accounts] login_for_access_token: Zerohertz                                                   accounts.py:43
                    DEBUG    [FastAPI] [crud] get_account_by_username: Zerohertz                                                                  crud.py:23
                    DEBUG    [FastAPI] [crud] _fetch_by_id: <class 'app.models.Account'>                                                          crud.py:28
                    DEBUG    [FastAPI] [auth] create_access_token: Zerohertz                                                                      auth.py:50
                    INFO     [FastAPI] [database] get_redis: Close                                                                            database.py:37
                    INFO     [FastAPI] [database] get_postgres: Close                                                                         database.py:27
INFO:     {IP}.{IP}.{IP}.{IP}:62486 - "POST /accounts/token/ HTTP/1.1" 200 OK
                    INFO     [FastAPI] [database] get_postgres: Connect                                                                       database.py:21
                    INFO     [FastAPI] [database] get_redis: Connect                                                                          database.py:31
                    DEBUG    [FastAPI] [auth] get_data: 3a260308848c80ae3078bf5390521396f65c13f48835c7b7b7c4a3f37a270c40                          auth.py:62
                    DEBUG    [FastAPI] [auth] get_data: Zerohertz                                                                                 auth.py:67
                    DEBUG    [FastAPI] [crud] get_account_by_username: Zerohertz                                                                  crud.py:23
                    DEBUG    [FastAPI] [crud] _fetch_by_id: <class 'app.models.Account'>                                                          crud.py:28
                    INFO     [FastAPI] [routers/accounts] read_account_me: Zerohertz                                                          accounts.py:33
                    INFO     [FastAPI] [database] get_redis: Close                                                                            database.py:37
                    INFO     [FastAPI] [database] get_postgres: Close                                                                         database.py:27
INFO:     {IP}.{IP}.{IP}.{IP}:62487 - "GET /accounts/me/ HTTP/1.1" 200 OK
```

---

### References

- [richard-to/kubernetes-experiments](https://github.com/richard-to/kubernetes-experiments/tree/master/authentication_api/app)

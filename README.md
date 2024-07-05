# Setup

```shell
kubectl create ns fastapi
kubectl apply -n fastapi -f k8s
kubectl exec -it -n fastapi deploy/fastapi -- zsh
```

## Database Migration

```shell
alembic init alembic
sed -i '1i\from app.config import settings\nfrom app.database import Base\n' alembic/env.py
sed -i 's|target_metadata = None|target_metadata = Base.metadata|g' alembic/env.py
sed -i '19i\config.set_main_option("sqlalchemy.url", settings.db_url)' alembic/env.py
isort alembic && black alembic
alembic revision --autogenerate -m "Init: Migration"
```

## FastAPI

```shell
uvicorn app.main:app --host 0.0.0.0
```

---

## References

- [richard-to/kubernetes-experiments](https://github.com/richard-to/kubernetes-experiments/tree/master/authentication_api/app)

# Setup

```shell
kubectl create ns fastapi
kubectl apply -n fastapi -f k8s
kubectl exec -it -n fastapi deploy/fastapi -- zsh
```

## Database Migration

```shell
pip install alembic
alembic init alembic
alembic revision --autogenerate -m "Initial migration"
```

---

## References

- [richard-to/kubernetes-experiments](https://github.com/richard-to/kubernetes-experiments/tree/master/authentication_api/app)

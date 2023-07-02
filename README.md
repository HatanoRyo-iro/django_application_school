# Chirp

このアプリはブログのようなものです。

# django-template

start project だけ実行してくれれば、あとはいつも通りの django で開発できます。
docker 内で行いたい場合は、docker compose exec app bash でコンテナに入ってください。

### start project

```bash
docker compose up -d
```

### stop project

```bash
docker compose down
```

### create app

```bash
docker compose exec app python manage.py startapp <app_name>
```

### create superuser

```bash
docker compose exec app python manage.py createsuperuser
```

### python のコンテナに入る (bash)

```bash
docker compose exec app bash
```

### python のコンテナから出る

```bash
exit
```

# Chirp

このアプリケーションはブログのようなものです。


### 1. 以下のコマンドを実行してください。

```bash
$ docker compose up --build

# djangoのマイグレーションを実行してください。（初回のみ）

$ docker compose exec app python manage.py migrate

# djangoの管理者アカウントを作成してください。（後で使用します。）

$ docker compose exec app python manage.py　createsuperuser

```

### 2. localhost:8000/adminに作成した管理者アカウントでアクセスしてください。

[http://localhost:8000/admin](http://localhost:8000/admin)

### 3. 管理者アカウントで設定を追加してください。




### 以下でアプリケーションを終了します。

```bash
docker compose down
```

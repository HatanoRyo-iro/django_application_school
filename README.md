# Chirp

このアプリケーションはブログのようなものです．


### 1. 以下のコマンドを実行してください．

```bash
$ docker compose up --build

# djangoのマイグレーションを実行してください．（初回のみ）

$ docker compose exec app python manage.py migrate

# データベースの初期情報を追加します

$ docker compose exec app python manage.py loaddata user.json

```

### 2. localhost:8000にアクセスしてください

[http://localhost:8000](http://localhost:8000)






### 3. 以下でアプリケーションを終了します。

```bash
docker compose down
```

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



## エラーが出た場合
```bash

# dockerを一回閉じてください

$ docker compose down

# 再びdockerを開いてください

$ docker compose up --build

# 続きから再開してください

open http://localhost:8000

```


### 3. 以下のコマンドでアプリケーションを終了します。

```bash
$ docker compose down
```

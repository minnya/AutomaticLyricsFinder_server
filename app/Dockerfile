# 使用するPythonのバージョンを指定
FROM python:3.9-slim

# 必要なパッケージをインストール
RUN pip install --no-cache-dir --upgrade pip

# 作業ディレクトリを設定
WORKDIR /app

# 必要なファイルをコンテナにコピー
COPY requirements.txt /app/

# 必要なライブラリをインストール
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションコードをコピー
COPY . /app/

# FastAPIを起動するためのコマンド
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

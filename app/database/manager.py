import os
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base

# 環境変数から接続情報を取得してSQLAlchemyのエンジンを初期化
engine = create_engine(
    f"mysql+pymysql://{os.getenv('MARIADB_USER')}:{os.getenv('MARIADB_PASSWORD')}@"
    f"{os.getenv('MARIADB_HOST')}/{os.getenv('MARIADB_DATABASE')}",
    echo=False,  # ログ出力を有効にする
    pool_recycle=3600,  # 1時間ごとに接続をリサイクル
)
# Sessionの作成
session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
# modelで使用する
Base = declarative_base()
Base.query = session.query_property()

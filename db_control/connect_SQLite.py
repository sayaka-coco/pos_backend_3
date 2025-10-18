from sqlalchemy import create_engine
import os

# データベースファイルのパス（backend直下に作成）
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_PATH = os.path.join(BASE_DIR, "pos_local.db")

# SQLiteのURL構築
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# エンジンの作成
engine = create_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=True,
)

print(f"SQLite Database: {DATABASE_PATH}")

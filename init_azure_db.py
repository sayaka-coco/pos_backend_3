"""Azure MySQL環境の初期化スクリプト"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import os
os.environ['USE_MYSQL'] = 'true'

from db_control.connect_MySQL import engine
from db_control import mymodels_MySQL as mymodels
from db_control import crud

print("=== Azure MySQLに接続中 ===")
print(f"Host: {os.getenv('DB_HOST')}")
print(f"Database: {os.getenv('DB_NAME')}")

# テーブル作成
print("\n=== テーブルを作成中 ===")
try:
    mymodels.Base.metadata.create_all(engine)
    print("OK テーブル作成完了")
except Exception as e:
    print(f"エラー: {e}")
    sys.exit(1)

# サンプル商品データ
sample_items = [
    {"item_id": "4901681517336", "item_name": "サラサクリップ 0.5 緑", "price": 110},
    {"item_id": "4901681517312", "item_name": "サラサクリップ 0.5 赤", "price": 110},
    {"item_id": "4901681517329", "item_name": "サラサクリップ 0.5 青", "price": 110},
    {"item_id": "4901681517305", "item_name": "サラサクリップ 0.5 黒", "price": 110},
    {"item_id": "4901681501113", "item_name": "ジェットストリーム 0.5 赤", "price": 132},
    {"item_id": "4901681501120", "item_name": "ジェットストリーム 0.5 青", "price": 132},
    {"item_id": "4901681501106", "item_name": "ジェットストリーム 0.5 黒", "price": 132},
    {"item_id": "4901681428120", "item_name": "ハイマッキー 赤", "price": 165},
    {"item_id": "4901681428137", "item_name": "ハイマッキー 青", "price": 165},
    {"item_id": "4901681428113", "item_name": "ハイマッキー 黒", "price": 165},
]

# デフォルト顧客を登録
print("\n=== デフォルト顧客を登録中 ===")
default_customer = {
    "customer_id": "0000",
    "customer_name": "ゲスト",
    "age": 0,
    "gender": "unknown"
}
try:
    crud.myinsert(mymodels.Customers, default_customer)
    print("OK デフォルト顧客登録完了")
except Exception as e:
    print(f"デフォルト顧客登録スキップ (既に存在): {str(e)[:50]}")

# 商品データ登録
print("\n=== 商品データを登録中 ===")
for item in sample_items:
    try:
        crud.myinsert(mymodels.Items, item)
        print(f"OK {item['item_name']} ({item['price']}円)")
    except Exception as e:
        print(f"スキップ {item['item_name']} - {str(e)[:30]}")

print("\n=== Azure MySQL初期化完了！ ===")

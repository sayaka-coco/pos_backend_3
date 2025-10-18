"""ローカルSQLite環境の初期化スクリプト"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from db_control.connect_SQLite import engine
from db_control import mymodels_MySQL as mymodels
from db_control import crud

# テーブル作成
print("=== テーブルを作成中 ===")
mymodels.Base.metadata.create_all(engine)
print("OK テーブル作成完了")

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
    print(f"デフォルト顧客登録スキップ (既に存在): {e}")

# 商品データ登録
print("\n=== 商品データを登録中 ===")
for item in sample_items:
    try:
        crud.myinsert(mymodels.Items, item)
        print(f"OK {item['item_name']} ({item['price']}円)")
    except Exception as e:
        print(f"NG {item['item_name']} - スキップ: {str(e)[:50]}")

print("\n=== 初期化完了！ ===")
print("バックエンドを起動してください: python -m uvicorn app:app --reload")

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import json
from db_control import crud, mymodels_MySQL as mymodels


app = FastAPI()


# CORSミドルウェアの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def index():
    return {"message": "POS Application API"}


# POS用エンドポイント
@app.get("/items/{item_id}")
def get_item(item_id: str):
    """商品コードで商品を検索"""
    Session = crud.sessionmaker(bind=crud.engine)
    session = Session()
    try:
        item = session.query(mymodels.Items).filter(mymodels.Items.item_id == item_id).first()
        if not item:
            raise HTTPException(status_code=404, detail="商品が見つかりません")
        return {
            "item_id": item.item_id,
            "item_name": item.item_name,
            "price": item.price
        }
    finally:
        session.close()


@app.get("/items")
def get_all_items():
    """全商品を取得"""
    result = crud.myselectAll(mymodels.Items)
    if not result:
        return []
    return json.loads(result)


class PurchaseRequest(BaseModel):
    customer_id: str = "0000"  # デフォルト顧客
    items: list[dict]  # [{"item_id": "1234567890", "quantity": 1}, ...]


@app.post("/purchases")
def create_purchase(purchase: PurchaseRequest):
    """購入処理"""
    from datetime import datetime
    Session = crud.sessionmaker(bind=crud.engine)
    session = Session()

    try:
        # 購入IDを生成（タイムスタンプベース）
        purchase_id = datetime.now().strftime("%Y%m%d%H%M%S")[:10]
        purchase_date = datetime.now().strftime("%Y-%m-%d")

        # 合計金額を事前計算
        total_amount = 0
        for item in purchase.items:
            item_data = session.query(mymodels.Items).filter(
                mymodels.Items.item_id == item["item_id"]
            ).first()
            if not item_data:
                raise HTTPException(status_code=404, detail=f"商品が見つかりません: {item['item_id']}")
            total_amount += item_data.price * item["quantity"]

        # 購入レコード作成（合計金額を含む）
        purchase_data = {
            "purchase_id": purchase_id,
            "customer_id": purchase.customer_id,
            "purchase_date": purchase_date,
            "total_amount": total_amount
        }
        crud.myinsert(mymodels.Purchases, purchase_data)

        # 購入詳細レコード作成
        for idx, item in enumerate(purchase.items):
            detail_data = {
                "detail_id": f"{purchase_id}{idx:02d}",
                "purchase_id": purchase_id,
                "item_id": item["item_id"],
                "quantity": item["quantity"]
            }
            crud.myinsert(mymodels.PurchaseDetails, detail_data)

        return {
            "purchase_id": purchase_id,
            "total_amount": total_amount,
            "purchase_date": purchase_date
        }

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()

@app.get("/db-check")
def db_check():
    try:
        db = SessionLocal()
        result = db.execute(text("SELECT 1")).fetchone()
        return {"status": "connected", "result": result[0]}
    except OperationalError as e:
        return {"status": "error", "details": str(e)}
    finally:
        db.close()

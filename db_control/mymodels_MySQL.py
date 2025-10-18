from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Customers(Base):
    __tablename__ = 'customers'
    customer_id: Mapped[str] = mapped_column(String(10), primary_key=True)
    customer_name: Mapped[str] = mapped_column(String(100))
    age: Mapped[int] = mapped_column(Integer)
    gender: Mapped[str] = mapped_column(String(10))


class Items(Base):
    __tablename__ = 'items'
    item_id: Mapped[str] = mapped_column(String(13), primary_key=True)  # JANコード(13桁)
    item_name: Mapped[str] = mapped_column(String(100))
    price: Mapped[int] = mapped_column(Integer)


class Purchases(Base):
    __tablename__ = 'purchases'
    purchase_id: Mapped[str] = mapped_column(String(10), primary_key=True)
    customer_id: Mapped[str] = mapped_column(String(10), ForeignKey("customers.customer_id"))
    purchase_date: Mapped[str] = mapped_column(String(10))
    total_amount: Mapped[int] = mapped_column(Integer)  # 合計金額（税込）


class PurchaseDetails(Base):
    __tablename__ = 'purchase_details'
    detail_id: Mapped[str] = mapped_column(String(20), primary_key=True)
    purchase_id: Mapped[str] = mapped_column(String(10), ForeignKey("purchases.purchase_id"))
    item_id: Mapped[str] = mapped_column(String(13), ForeignKey("items.item_id"))
    quantity: Mapped[int] = mapped_column(Integer)
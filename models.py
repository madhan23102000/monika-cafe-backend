from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    ForeignKey
)

from database import Base


# User Table
class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String(100)
    )

    email = Column(
        String(100),
        unique=True
    )

    password = Column(
        String(255)
    )

    role = Column(
        String(50)
    )


# Menu Table
class Menu(Base):
    __tablename__ = "menu"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String(100)
    )

    category = Column(
        String(100)
    )

    price = Column(
        Float
    )

    availability = Column(
        String(50)
    )


# Order Table
class Order(Base):
    __tablename__ = "orders"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    customer_name = Column(
        String(100)
    )

    menu_id = Column(
        Integer,
        ForeignKey("menu.id")
    )

    quantity = Column(
        Integer
    )

    total_price = Column(
        Float
    )

    status = Column(
        String(50),
        default="Pending"
    )



# Bill Table
class Bill(Base):
    __tablename__ = "bills"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    order_id = Column(
        Integer,
        ForeignKey("orders.id")
    )

    subtotal = Column(
        Float
    )

    gst = Column(
        Float
    )

    total = Column(
        Float
    )

    payment_method = Column(
        String(50)
    )

    payment_status = Column(
        String(50),
        default="Paid"
    )

class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    item_name = Column(
        String(100)
    )

    quantity = Column(
        Integer
    )

    supplier = Column(
        String(100)
    )

    status = Column(
        String(50)
    )
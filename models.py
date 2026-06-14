from sqlalchemy import (
    Column,
    Integer,
    String,
    Float
)

from database import Base


# ======================
# USER TABLE
# ======================

class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(String(100))

    email = Column(
        String(100),
        unique=True
    )

    password = Column(
        String(255)
    )

    role = Column(
        String(50),
        default="customer"
    )


# ======================
# MENU TABLE
# ======================

class Menu(Base):
    __tablename__ = "menu"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(String(100))

    category = Column(String(100))

    price = Column(Float)

    availability = Column(
        String(50)
    )


# ======================
# ORDER TABLE
# ======================

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

    item = Column(
        String(100)
    )

    quantity = Column(
        Integer
    )

    status = Column(
        String(50),
        default="Pending"
    )


# ======================
# BILL TABLE
# ======================

class Bill(Base):
    __tablename__ = "bills"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    order_id = Column(
        Integer
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

    status = Column(
        String(50),
        default="Paid"
    )


# ======================
# INVENTORY TABLE
# ======================

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


# ======================
# CUSTOMER TABLE
# ======================

class Customer(Base):
    __tablename__ = "customers"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String(100)
    )

    phone = Column(
        String(20)
    )

    address = Column(
        String(255)
    )

    loyalty_points = Column(
        Integer,
        default=0
    )

# ======================
# RESERVATION TABLE
# ======================

class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    customer_name = Column(
        String(100)
    )

    table_number = Column(
        Integer
    )

    date = Column(
        String(50)
    )

    time = Column(
        String(50)
    )

    status = Column(
        String(50),
        default="Booked"
    )

# ======================
# FEEDBACK TABLE
# ======================

class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    customer_name = Column(
        String(100)
    )

    rating = Column(
        Integer
    )

    review = Column(
        String(500)
    )

    status = Column(
        String(50),
        default="Open"
    )

# ======================
# EMPLOYEE TABLE
# ======================

class Employee(Base):
    __tablename__ = "employees"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String(100)
    )

    role = Column(
        String(100)
    )

    salary = Column(
        Float
    )

    attendance = Column(
        String(50),
        default="Present"
    )
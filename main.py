from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt

from database import (
    SessionLocal,
    engine,
    Base
)

from models import (
    User,
    Menu,
    Order,
    Bill,
    Inventory
)

from schemas import (
    UserCreate,
    UserLogin,
    MenuCreate,
    MenuUpdate,
    OrderCreate,
    OrderStatusUpdate,
    BillCreate,
    InventoryCreate,
    InventoryUpdate
)

# Create Tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Security
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

SECRET_KEY = "monika_cafe_secret_key"
ALGORITHM = "HS256"


# Database
def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# HOME
@app.get("/")
def home():

    return {
        "message": "Monika Cafe Backend"
    }


# TEST
@app.get("/test")
def test():

    return {
        "status": "working"
    }


# REGISTER
@app.post("/register")
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    existing = db.query(
        User
    ).filter(
        User.email == user.email
    ).first()

    if existing:

        return {
            "message": "Email Exists"
        }

    hashed = pwd_context.hash(
        user.password
    )

    new_user = User(
        name=user.name,
        email=user.email,
        password=hashed,
        role=user.role
    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    return {
        "message": "Registered",
        "id": new_user.id
    }


# LOGIN
@app.post("/login")
def login(
    user: UserLogin,
    db: Session = Depends(get_db)
):

    db_user = db.query(
        User
    ).filter(
        User.email == user.email
    ).first()

    if not db_user:

        return {
            "message": "User Not Found"
        }

    if not pwd_context.verify(
        user.password,
        db_user.password
    ):

        return {
            "message": "Wrong Password"
        }

    token = jwt.encode(
        {
            "sub": db_user.email
        },

        SECRET_KEY,

        algorithm=ALGORITHM
    )

    return {
        "access_token": token
    }


# MENU ADD
@app.post("/menu")
def add_menu(
    menu: MenuCreate,
    db: Session = Depends(get_db)
):

    item = Menu(**menu.dict())

    db.add(item)

    db.commit()

    db.refresh(item)

    return {
        "message": "Menu Added"
    }


# VIEW MENU
@app.get("/menu")
def view_menu(
    db: Session = Depends(get_db)
):

    return db.query(
        Menu
    ).all()


# UPDATE MENU
@app.put("/menu/{menu_id}")
def update_menu(
    menu_id: int,
    menu: MenuUpdate,
    db: Session = Depends(get_db)
):

    item = db.query(
        Menu
    ).filter(
        Menu.id == menu_id
    ).first()

    if not item:

        return {
            "message": "Not Found"
        }

    item.name = menu.name
    item.category = menu.category
    item.price = menu.price
    item.availability = menu.availability

    db.commit()

    return {
        "message": "Updated"
    }


# DELETE MENU
@app.delete("/menu/{menu_id}")
def delete_menu(
    menu_id: int,
    db: Session = Depends(get_db)
):

    item = db.query(
        Menu
    ).filter(
        Menu.id == menu_id
    ).first()

    if item:

        db.delete(item)

        db.commit()

    return {
        "message": "Deleted"
    }


# PLACE ORDER
@app.post("/order")
def place_order(
    order: OrderCreate,
    db: Session = Depends(get_db)
):

    menu = db.query(
        Menu
    ).filter(
        Menu.id == order.menu_id
    ).first()

    if not menu:

        return {
            "message": "Menu Not Found"
        }

    total = (
        menu.price *
        order.quantity
    )

    obj = Order(
        customer_name=order.customer_name,
        menu_id=order.menu_id,
        quantity=order.quantity,
        total_price=total,
        status="Pending"
    )

    db.add(obj)

    db.commit()

    return {
        "message": "Order Success"
    }


# VIEW ORDER
@app.get("/orders")
def orders(
    db: Session = Depends(get_db)
):

    return db.query(
        Order
    ).all()


# UPDATE ORDER
@app.put("/orders/{order_id}")
def update_order(
    order_id: int,
    data: OrderStatusUpdate,
    db: Session = Depends(get_db)
):

    obj = db.query(
        Order
    ).filter(
        Order.id == order_id
    ).first()

    if not obj:

        return {
            "message": "Not Found"
        }

    obj.status = data.status

    db.commit()

    return {
        "message": "Updated"
    }


# BILL
@app.post("/bill")
def bill(
    data: BillCreate,
    db: Session = Depends(get_db)
):

    order = db.query(
        Order
    ).filter(
        Order.id == data.order_id
    ).first()

    subtotal = order.total_price

    gst = subtotal * 0.05

    total = subtotal + gst

    obj = Bill(
        order_id=data.order_id,
        subtotal=subtotal,
        gst=gst,
        total=total,
        payment_method=data.payment_method
    )

    db.add(obj)

    db.commit()

    return {
        "total": total
    }


@app.get("/bill")
def view_bill(
    db: Session = Depends(get_db)
):

    return db.query(
        Bill
    ).all()


# INVENTORY
@app.post("/inventory")
def add_inventory(
    data: InventoryCreate,
    db: Session = Depends(get_db)
):

    obj = Inventory(**data.dict())

    db.add(obj)

    db.commit()

    return {
        "message": "Inventory Added"
    }


@app.get("/inventory")
def inventory(
    db: Session = Depends(get_db)
):

    return db.query(
        Inventory
    ).all()
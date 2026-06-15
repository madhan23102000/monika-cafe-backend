from fastapi import HTTPException
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt
from fastapi.responses import FileResponse

from reportlab.pdfgen import canvas


from database import SessionLocal, engine, Base

from models import (
User,
Menu,
Order,
Bill,
Inventory,
Customer,
Reservation,
Feedback,
Employee
)

from schemas import (
UserCreate,
UserLogin,
MenuCreate,
MenuUpdate,
OrderCreate,
OrderUpdate,
BillCreate,
InventoryCreate,
CustomerCreate,
CustomerUpdate,
ReservationCreate,
ReservationUpdate,
FeedbackCreate,
FeedbackUpdate,
EmployeeCreate,
EmployeeUpdate,
)

Base.metadata.create_all(bind=engine)

app = FastAPI()

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

SECRET_KEY = "monika_cafe_secret_key"
ALGORITHM = "HS256"


# ======================
# DATABASE
# ======================

def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# ======================
# HOME
# ======================

@app.get("/")
def home():
    return {
        "message": "Monika Cafe Backend Running"
    }


# ======================
# REGISTER
# ======================

@app.post("/register")
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):

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

    return {
        "message": "Registered"
    }


# ======================
# LOGIN
# ======================

@app.post("/login")
def login(
    user: UserLogin,
    db: Session = Depends(get_db)
):

    db_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if not db_user:
        return {
            "message": "User not found"
        }

    if not pwd_context.verify(
        user.password,
        db_user.password
    ):
        return {
            "message": "Invalid Password"
        }

    token = jwt.encode(
        {
            "email": db_user.email,
            "role": db_user.role
        },
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return {
        "token": token
    }


# ======================
# MENU
# ======================

@app.post("/menu")
def add_menu(
    menu: MenuCreate,
    db: Session = Depends(get_db)
):

    item = Menu(**menu.model_dump())

    db.add(item)

    db.commit()

    return {
        "message": "Menu Added"
    }


@app.get("/menu")
def view_menu(
    db: Session = Depends(get_db)
):

    return db.query(Menu).all()


# ======================
# ORDER
# ======================

@app.post("/order")
def create_order(
    order: OrderCreate,
    db: Session = Depends(get_db)
):

    new_order = Order(**order.model_dump())

    db.add(new_order)

    db.commit()

    db.refresh(new_order)

    return {
        "message": "Order Created",
        "order_id": new_order.id
    }


@app.get("/order")
def view_orders(
    db: Session = Depends(get_db)
):

    return db.query(Order).all()


@app.put("/order/{order_id}")
def update_order(
    order_id: int,
    order: OrderUpdate,
    db: Session = Depends(get_db)
):

    item = db.query(Order).filter(
        Order.id == order_id
    ).first()

    item.status = order.status

    db.commit()

    return {
        "message": "Updated"
    }


# ======================
# BILL
# ======================

# ======================
# BILL
# ======================

@app.post("/bill")
def create_bill(
    bill: BillCreate,
    db: Session = Depends(get_db)
):

    gst = bill.subtotal * 0.05

    total = bill.subtotal + gst

    data = Bill(
        order_id=bill.order_id,
        subtotal=bill.subtotal,
        gst=gst,
        total=total,
        payment_method=bill.payment_method
    )

    db.add(data)

    # -------------------
    # LOYALTY POINTS
    # ₹100 = 10 points
    # -------------------

    customer = db.query(
        Customer
    ).first()

    if customer:

        points = (
            int(
                bill.subtotal / 100
            ) * 10
        )

        customer.loyalty_points += points

    db.commit()

    db.refresh(data)

    return {
        "message": "Bill Created",
        "bill_id": data.id,
        "subtotal": bill.subtotal,
        "gst": gst,
        "total": total,
        "loyalty_added": (
            int(
                bill.subtotal / 100
            ) * 10
        )
    }
# ======================
# INVENTORY
# ======================

@app.post("/inventory")
def add_inventory(
    inventory: InventoryCreate,
    db: Session = Depends(get_db)
):

    item = Inventory(
        **inventory.model_dump()
    )

    db.add(item)

    db.commit()

    return {
        "message": "Inventory Added"
    }


@app.get("/inventory")
def view_inventory(
    db: Session = Depends(get_db)
):

    return db.query(
        Inventory
    ).all()


# ======================
# CUSTOMER
# ======================

@app.post("/customer")
def create_customer(
    customer: CustomerCreate,
    db: Session = Depends(get_db)
):

    data = Customer(
        **customer.model_dump()
    )

    db.add(data)

    db.commit()

    return {
        "message": "Customer Added"
    }


@app.get("/customer")
def view_customer(
    db: Session = Depends(get_db)
):

    return db.query(
        Customer
    ).all()


@app.get("/customer/{customer_id}")
def get_customer(
    customer_id: int,
    db: Session = Depends(get_db)
):

    return db.query(
        Customer
    ).filter(
        Customer.id == customer_id
    ).first()


@app.put("/customer/{customer_id}")
def update_customer(
    customer_id: int,
    customer: CustomerUpdate,
    db: Session = Depends(get_db)
):

    data = db.query(
        Customer
    ).filter(
        Customer.id == customer_id
    ).first()

    data.name = customer.name
    data.phone = customer.phone
    data.address = customer.address
    data.loyalty_points = customer.loyalty_points

    db.commit()

    return {
        "message": "Customer Updated"
    }

# ======================
# REPORTS
# ======================

@app.get("/reports/sales")
def sales_report(
    db: Session = Depends(get_db)
):

    total_orders = db.query(
        Order
    ).count()

    total_customers = db.query(
        Customer
    ).count()

    total_bills = db.query(
        Bill
    ).count()

    return {
        "total_orders": total_orders,
        "total_customers": total_customers,
        "total_bills": total_bills
    }


@app.get("/reports/revenue")
def revenue_report(
    db: Session = Depends(get_db)
):

    bills = db.query(
        Bill
    ).all()

    revenue = sum(
        bill.total
        for bill in bills
    )

    return {
        "total_revenue": revenue
    }


@app.get("/reports/orders")
def order_report(
    db: Session = Depends(get_db)
):

    return db.query(
        Order
    ).all()


@app.get("/reports/customers")
def customer_report(
    db: Session = Depends(get_db)
):

    return db.query(
        Customer
    ).all()

# ======================
# RESERVATION
# ======================

@app.post("/reservation")
def create_reservation(
    reservation: ReservationCreate,
    db: Session = Depends(get_db)
):

    data = Reservation(
        **reservation.model_dump()
    )

    db.add(data)

    db.commit()

    db.refresh(data)

    return {
        "message": "Reservation Created",
        "reservation_id": data.id
    }


@app.get("/reservation")
def view_reservation(
    db: Session = Depends(get_db)
):

    return db.query(
        Reservation
    ).all()


@app.put("/reservation/{reservation_id}")
def update_reservation(
    reservation_id: int,
    reservation: ReservationUpdate,
    db: Session = Depends(get_db)
):

    data = db.query(
        Reservation
    ).filter(
        Reservation.id == reservation_id
    ).first()

    if not data:

        return {
            "message": "Reservation Not Found"
        }

    data.status = reservation.status

    db.commit()

    return {
        "message": "Reservation Updated"
    }


@app.delete("/reservation/{reservation_id}")
def delete_reservation(
    reservation_id: int,
    db: Session = Depends(get_db)
):

    data = db.query(
        Reservation
    ).filter(
        Reservation.id == reservation_id
    ).first()

    if not data:

        return {
            "message": "Reservation Not Found"
        }

    db.delete(data)

    db.commit()

    return {
        "message": "Reservation Deleted"
    }

# ======================
# FEEDBACK
# ======================

@app.post("/feedback")
def create_feedback(
    feedback: FeedbackCreate,
    db: Session = Depends(get_db)
):

    data = Feedback(
        **feedback.model_dump()
    )

    db.add(data)

    db.commit()

    db.refresh(data)

    return {
        "message": "Feedback Added",
        "feedback_id": data.id
    }


@app.get("/feedback")
def view_feedback(
    db: Session = Depends(get_db)
):

    return db.query(
        Feedback
    ).all()


@app.put("/feedback/{feedback_id}")
def update_feedback(
    feedback_id: int,
    feedback: FeedbackUpdate,
    db: Session = Depends(get_db)
):

    data = db.query(
        Feedback
    ).filter(
        Feedback.id == feedback_id
    ).first()

    if not data:

        return {
            "message": "Feedback Not Found"
        }

    data.status = feedback.status

    db.commit()

    return {
        "message": "Feedback Updated"
    }


@app.delete("/feedback/{feedback_id}")
def delete_feedback(
    feedback_id: int,
    db: Session = Depends(get_db)
):

    data = db.query(
        Feedback
    ).filter(
        Feedback.id == feedback_id
    ).first()

    if not data:

        return {
            "message": "Feedback Not Found"
        }

    db.delete(data)

    db.commit()

    return {
        "message": "Feedback Deleted"
    }

# ======================
# EMPLOYEE
# ======================

@app.post("/employee")
def create_employee(
    employee: EmployeeCreate,
    db: Session = Depends(get_db)
):

    data = Employee(
        **employee.model_dump()
    )

    db.add(data)

    db.commit()

    db.refresh(data)

    return {
        "message": "Employee Added",
        "employee_id": data.id
    }


@app.get("/employee")
def view_employee(
    db: Session = Depends(get_db)
):

    return db.query(
        Employee
    ).all()


@app.put("/employee/{employee_id}")
def update_employee(
    employee_id: int,
    employee: EmployeeUpdate,
    db: Session = Depends(get_db)
):

    data = db.query(
        Employee
    ).filter(
        Employee.id == employee_id
    ).first()

    if not data:
        return {
            "message": "Employee Not Found"
        }

    data.attendance = employee.attendance

    db.commit()

    return {
        "message": "Employee Updated"
    }


@app.delete("/employee/{employee_id}")
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db)
):

    data = db.query(
        Employee
    ).filter(
        Employee.id == employee_id
    ).first()

    if not data:
        return {
            "message": "Employee Not Found"
        }

    db.delete(data)

    db.commit()

    return {
        "message": "Employee Deleted"
    }

# ======================
# INVOICE PDF
# ======================

@app.get("/invoice/{bill_id}")
def download_invoice(
    bill_id: int,
    db: Session = Depends(get_db)
):

    bill = db.query(
        Bill
    ).filter(
        Bill.id == bill_id
    ).first()

    if not bill:

        return {
            "message": "Bill Not Found"
        }

    filename = f"invoice_{bill_id}.pdf"

    pdf = canvas.Canvas(
        filename
    )

    pdf.drawString(
        100,
        800,
        "MONIKA CAFE INVOICE"
    )

    pdf.drawString(
        100,
        760,
        f"Bill ID: {bill.id}"
    )

    pdf.drawString(
        100,
        730,
        f"Order ID: {bill.order_id}"
    )

    pdf.drawString(
        100,
        700,
        f"Subtotal: {bill.subtotal}"
    )

    pdf.drawString(
        100,
        670,
        f"GST: {bill.gst}"
    )

    pdf.drawString(
        100,
        640,
        f"Total: {bill.total}"
    )

    pdf.drawString(
        100,
        610,
        f"Payment: {bill.payment_method}"
    )

    pdf.save()

    return FileResponse(
        filename,
        media_type="application/pdf",
        filename=filename
    )

# ======================
# EMAIL
# ======================

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("havocmadhan200@gmail.com"),
    MAIL_PASSWORD=os.getenv("ggaghtubupgkuwom"),
    MAIL_FROM=os.getenv("havocmadhan200@gmail.com"),

    MAIL_SERVER="smtp.gmail.com",
    MAIL_PORT=587,

    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,

    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)


@app.post("/send-email")
async def send_email():

    try:
        message = MessageSchema(
            subject="Monika Cafe",
            recipients=["havocmadhan200@gmail.com"],
            body="Testing SMTP",
            subtype="plain"
        )

        fm = FastMail(conf)

        await fm.send_message(message)

        return {
            "message": "Email Sent Successfully"
        }

    except Exception as e:

        return {
            "error_type": str(type(e)),
            "error": str(e)
        }
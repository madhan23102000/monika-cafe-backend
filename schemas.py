from pydantic import BaseModel


# ======================
# USER SCHEMAS
# ======================

class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    role: str = "customer"


class UserLogin(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str

    class Config:
        from_attributes = True


# ======================
# MENU SCHEMAS
# ======================

class MenuCreate(BaseModel):
    name: str
    category: str
    price: float
    availability: str


class MenuUpdate(BaseModel):
    name: str
    category: str
    price: float
    availability: str


class MenuResponse(BaseModel):
    id: int
    name: str
    category: str
    price: float
    availability: str

    class Config:
        from_attributes = True


# ======================
# ORDER SCHEMAS
# ======================

class OrderCreate(BaseModel):
    customer_name: str
    item: str
    quantity: int


class OrderUpdate(BaseModel):
    status: str


class OrderResponse(BaseModel):
    id: int
    customer_name: str
    item: str
    quantity: int
    status: str

    class Config:
        from_attributes = True


# ======================
# BILL SCHEMAS
# ======================

class BillCreate(BaseModel):
    order_id: int
    subtotal: float
    payment_method: str


class BillResponse(BaseModel):
    id: int
    order_id: int
    subtotal: float
    gst: float
    total: float
    payment_method: str
    status: str

    class Config:
        from_attributes = True


# ======================
# INVENTORY SCHEMAS
# ======================

class InventoryCreate(BaseModel):
    item_name: str
    quantity: int
    supplier: str


class InventoryResponse(BaseModel):
    id: int
    item_name: str
    quantity: int
    supplier: str

    class Config:
        from_attributes = True


# ======================
# CUSTOMER SCHEMAS
# ======================

class CustomerCreate(BaseModel):
    name: str
    phone: str
    address: str


class CustomerUpdate(BaseModel):
    name: str
    phone: str
    address: str
    loyalty_points: int


class CustomerResponse(BaseModel):
    id: int
    name: str
    phone: str
    address: str
    loyalty_points: int

    class Config:
        from_attributes = True

# ======================
# RESERVATION SCHEMAS
# ======================

class ReservationCreate(BaseModel):
    customer_name: str
    table_number: int
    date: str
    time: str


class ReservationUpdate(BaseModel):
    status: str


class ReservationResponse(BaseModel):
    id: int
    customer_name: str
    table_number: int
    date: str
    time: str
    status: str

    class Config:
        from_attributes = True

# ======================
# FEEDBACK SCHEMAS
# ======================

class FeedbackCreate(BaseModel):
    customer_name: str
    rating: int
    review: str


class FeedbackUpdate(BaseModel):
    status: str


class FeedbackResponse(BaseModel):
    id: int
    customer_name: str
    rating: int
    review: str
    status: str

    class Config:
        from_attributes = True

# ======================
# EMPLOYEE SCHEMAS
# ======================

class EmployeeCreate(BaseModel):
    name: str
    role: str
    salary: float


class EmployeeUpdate(BaseModel):
    attendance: str


class EmployeeResponse(BaseModel):
    id: int
    name: str
    role: str
    salary: float
    attendance: str

    class Config:
        from_attributes = True

# ======================
# EMAIL SCHEMAS
# ======================

class EmailSchema(BaseModel):
    email: str
    subject: str
    message: str
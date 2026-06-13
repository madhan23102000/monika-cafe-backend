from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    role: str


class UserLogin(BaseModel):
    email: str
    password: str


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


class OrderCreate(BaseModel):
    customer_name: str
    menu_id: int
    quantity: int


class OrderStatusUpdate(BaseModel):
    status: str


class BillCreate(BaseModel):
    order_id: int
    payment_method: str

class InventoryCreate(BaseModel):
    item_name: str
    quantity: int
    supplier: str
    status: str


class InventoryUpdate(BaseModel):
    item_name: str
    quantity: int
    supplier: str
    status: str
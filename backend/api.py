from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from database import get_db
from models import Product, Contact
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/api", tags=["public"])

# Pydantic models
class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float
    material: str
    colour: str
    gsm: str
    width: str
    images: List[str]
    is_bestseller: bool
    
    class Config:
        from_attributes = True

class ContactRequest(BaseModel):
    name: str
    phone: str
    email: str
    subject: str
    message: str

class ReviewResponse(BaseModel):
    name: str
    text: str
    rating: int

@router.get("/products", response_model=List[ProductResponse])
def get_products(
    material: Optional[str] = None,
    colour: Optional[str] = None,
    price_min: Optional[float] = None,
    price_max: Optional[float] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Product)
    
    if material:
        query = query.filter(Product.material == material)
    if colour:
        query = query.filter(Product.colour == colour)
    if price_min is not None:
        query = query.filter(Product.price >= price_min)
    if price_max is not None:
        query = query.filter(Product.price <= price_max)
    
    products = query.all()
    return products

@router.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.get("/bestsellers", response_model=List[ProductResponse])
def get_bestsellers(db: Session = Depends(get_db)):
    products = db.query(Product).filter(Product.is_bestseller == True).limit(4).all()
    return products

@router.get("/reviews", response_model=List[ReviewResponse])
def get_reviews():
    # Static reviews as requested
    reviews = [
        {"name": "Sarah M.", "text": "Absolutely stunning fabrics! The quality exceeded my expectations.", "rating": 5},
        {"name": "James K.", "text": "Fast shipping and beautiful materials. Will order again!", "rating": 5},
        {"name": "Priya R.", "text": "The swatch kit was so helpful. Made choosing easy.", "rating": 4},
        {"name": "Emma L.", "text": "Beautiful linen that drapes perfectly. Highly recommend!", "rating": 5},
        {"name": "Michael T.", "text": "Great selection and excellent customer service.", "rating": 5}
    ]
    return reviews

@router.post("/contact")
def create_contact(contact: ContactRequest, db: Session = Depends(get_db)):
    new_contact = Contact(
        name=contact.name,
        phone=contact.phone,
        email=contact.email,
        subject=contact.subject,
        message=contact.message
    )
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)
    return {"message": "Contact form submitted successfully", "id": new_contact.id}

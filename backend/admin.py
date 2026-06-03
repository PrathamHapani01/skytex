from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Product, Contact, Admin
from auth import authenticate_admin, create_access_token, get_current_admin, get_password_hash
from pydantic import BaseModel
from datetime import timedelta
import os
import uuid
from pathlib import Path

# Cloudinary imports
import cloudinary
import cloudinary.uploader

router = APIRouter(prefix="/api/admin", tags=["admin"])

# Allowed file extensions (optional, keep for safety)
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

# Pydantic models
class AdminLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    material: str
    colour: str
    gsm: str
    width: str
    images: List[str]
    is_bestseller: bool = False

class ProductUpdate(BaseModel):
    name: str = None
    description: str = None
    price: float = None
    material: str = None
    colour: str = None
    gsm: str = None
    width: str = None
    images: List[str] = None
    is_bestseller: bool = None

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

class ContactResponse(BaseModel):
    id: int
    name: str
    phone: str
    email: str
    subject: str
    message: str
    created_at: str
    
    class Config:
        from_attributes = True

@router.post("/login", response_model=Token)
def admin_login(login_data: AdminLogin, db: Session = Depends(get_db)):
    admin = authenticate_admin(db, login_data.username, login_data.password)
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": admin.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/products", response_model=List[ProductResponse])
def get_all_products(db: Session = Depends(get_db), current_admin: Admin = Depends(get_current_admin)):
    products = db.query(Product).all()
    return products

@router.post("/products", response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db), current_admin: Admin = Depends(get_current_admin)):
    new_product = Product(
        name=product.name,
        description=product.description,
        price=product.price,
        material=product.material,
        colour=product.colour,
        gsm=product.gsm,
        width=product.width,
        images=product.images,
        is_bestseller=product.is_bestseller
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@router.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db), current_admin: Admin = Depends(get_current_admin)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/products/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product: ProductUpdate, db: Session = Depends(get_db), current_admin: Admin = Depends(get_current_admin)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    update_data = product.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_product, key, value)
    
    db.commit()
    db.refresh(db_product)
    return db_product

@router.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db), current_admin: Admin = Depends(get_current_admin)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return {"message": "Product deleted successfully"}

@router.get("/contacts", response_model=List[ContactResponse])
def get_contacts(db: Session = Depends(get_db), current_admin: Admin = Depends(get_current_admin)):
    contacts = db.query(Contact).order_by(Contact.created_at.desc()).all()
    return contacts

@router.post("/upload-image")
async def upload_image(
    file: UploadFile = File(...),
    current_admin: Admin = Depends(get_current_admin)
):
    # Validate file extension (optional)
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # Read file content (for size check)
    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Max {MAX_FILE_SIZE // (1024*1024)}MB"
        )
    
    # Configure Cloudinary from environment variables
    cloudinary.config(
        cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
        api_key=os.getenv("CLOUDINARY_API_KEY"),
        api_secret=os.getenv("CLOUDINARY_API_SECRET"),
        secure=True
    )
    
    try:
        # Upload to Cloudinary
        upload_result = cloudinary.uploader.upload(contents)
        file_url = upload_result['secure_url']
        return {"url": file_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cloudinary upload failed: {str(e)}")
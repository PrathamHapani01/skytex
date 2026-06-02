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

router = APIRouter(prefix="/api/admin", tags=["admin"])

# Configure upload directory
# WARNING: Render uses ephemeral filesystem — uploads are lost on redeploy.
# For persistent storage, integrate a cloud provider (S3, Cloudinary, etc.)
UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", "/app/uploads"))
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Allowed file extensions
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
    # Validate file extension
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # Generate unique filename
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    file_path = UPLOAD_DIR / unique_filename
    
    # Save file
    try:
        contents = await file.read()
        if len(contents) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Maximum size is {MAX_FILE_SIZE / (1024*1024)}MB"
            )
        
        with open(file_path, "wb") as f:
            f.write(contents)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")
    
    # Return the URL to access the uploaded file
    return {"url": f"/uploads/{unique_filename}"}

import os
from dotenv import load_dotenv

# Load .env so DATABASE_URL is available when run standalone
load_dotenv()

from database import SessionLocal, Base, engine
from models import Product, Admin
from auth import get_password_hash

# Create tables
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Read admin credentials from environment (with defaults for first setup)
admin_username = os.getenv("ADMIN_USERNAME", "admin")
admin_password = os.getenv("ADMIN_PASSWORD", "admin123")

# Check if admin exists, if not create default admin
existing_admin = db.query(Admin).filter(Admin.username == admin_username).first()
if not existing_admin:
    admin = Admin(
        username=admin_username,
        hashed_password=get_password_hash(admin_password)
    )
    db.add(admin)
    db.commit()
    print(f"Created admin: username={admin_username}")
else:
    print(f"Admin '{admin_username}' already exists")

# Check if products exist, if not seed them
existing_products = db.query(Product).count()
if existing_products == 0:
    products = [
        {
            "name": "Premium Linen Fabric",
            "price": 450,
            "material": "Linen",
            "colour": "Beige",
            "gsm": "180 gsm",
            "width": "150 cm",
            "description": "Breathable, high-quality linen perfect for summer wear. Natural texture with excellent drape.",
            "images": [
                "https://images.unsplash.com/photo-1520006403909-838d6b92c22e?w=600",
                "https://images.unsplash.com/photo-1558171813-4c088753af8f?w=600",
                "https://images.unsplash.com/photo-1596462502278-27bfdd403348?w=600"
            ],
            "is_bestseller": True
        },
        {
            "name": "Soft Cotton Blend",
            "price": 320,
            "material": "Cotton",
            "colour": "White",
            "gsm": "160 gsm",
            "width": "140 cm",
            "description": "Soft, comfortable cotton blend ideal for everyday use. Durable and easy to care for.",
            "images": [
                "https://images.unsplash.com/photo-1558171813-4c088753af8f?w=600",
                "https://images.unsplash.com/photo-1520006403909-838d6b92c22e?w=600",
                "https://images.unsplash.com/photo-1576566588028-4147f3842f27?w=600"
            ],
            "is_bestseller": True
        },
        {
            "name": "Luxury Silk",
            "price": 890,
            "material": "Silk",
            "colour": "Champagne",
            "gsm": "90 gsm",
            "width": "114 cm",
            "description": "Elegant silk with champagne sheen and soft drape. Perfect for special occasions.",
            "images": [
                "https://images.unsplash.com/photo-1596462502278-27bfdd403348?w=600",
                "https://images.unsplash.com/photo-1520006403909-838d6b92c22e?w=600",
                "https://images.unsplash.com/photo-1558171813-4c088753af8f?w=600"
            ],
            "is_bestseller": True
        },
        {
            "name": "Warm Wool",
            "price": 550,
            "material": "Wool",
            "colour": "Grey",
            "gsm": "280 gsm",
            "width": "150 cm",
            "description": "Cozy wool and cashmere blend for winter warmth. Soft to touch with excellent insulation.",
            "images": [
                "https://images.unsplash.com/photo-1576566588028-4147f3842f27?w=600",
                "https://images.unsplash.com/photo-1520006403909-838d6b92c22e?w=600",
                "https://images.unsplash.com/photo-1558171813-4c088753af8f?w=600"
            ],
            "is_bestseller": True
        },
        {
            "name": "Premium Digital Print Fabric",
            "price": 420,
            "material": "Cotton",
            "colour": "Multi",
            "gsm": "150 gsm",
            "width": "145 cm",
            "description": "High-quality digital print fabric with vibrant colors and intricate patterns. Perfect for fashion and home decor.",
            "images": [
                "assets/download.webp",
                "https://images.unsplash.com/photo-1520006403909-838d6b92c22e?w=600",
                "https://images.unsplash.com/photo-1558171813-4c088753af8f?w=600"
            ],
            "is_bestseller": False
        },
        {
            "name": "Premium Tapeta Fabric",
            "price": 680,
            "material": "Tapeta",
            "colour": "Navy",
            "gsm": "320 gsm",
            "width": "140 cm",
            "description": "Luxurious tapeta fabric with elegant texture and rich color. Perfect for upholstery and premium home decor.",
            "images": [
                "https://images.unsplash.com/photo-1576566588028-4147f3842f27?w=600",
                "https://images.unsplash.com/photo-1520006403909-838d6b92c22e?w=600",
                "https://images.unsplash.com/photo-1558171813-4c088753af8f?w=600"
            ],
            "is_bestseller": False
        }
    ]
    
    for product_data in products:
        product = Product(**product_data)
        db.add(product)
    
    db.commit()
    print(f"Seeded {len(products)} products")
else:
    print(f"Database already has {existing_products} products")

db.close()
print("Seed completed successfully")

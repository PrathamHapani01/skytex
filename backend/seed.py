import os
from dotenv import load_dotenv

load_dotenv()

from database import SessionLocal, engine, Base
from models import Product, Admin
from auth import get_password_hash

def seed_database():
    """Create tables, admin user, and initial products if they don't exist."""
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("Tables created/verified.")
    
    db = SessionLocal()
    try:
        # ---- Admin ----
        admin_username = os.getenv("ADMIN_USERNAME", "admin")
        admin_password = os.getenv("ADMIN_PASSWORD", "admin123")
        existing_admin = db.query(Admin).filter(Admin.username == admin_username).first()
        if not existing_admin:
            admin = Admin(
                username=admin_username,
                hashed_password=get_password_hash(admin_password)
            )
            db.add(admin)
            db.commit()
            print(f"✅ Admin '{admin_username}' created.")
        else:
            print(f"ℹ️ Admin '{admin_username}' already exists.")
        
        # ---- Products (seed only if table is empty) ----
        if db.query(Product).count() == 0:
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
                        "https://images.unsplash.com/photo-1520006403909-838d6b92c22e?w=600",
                        "https://images.unsplash.com/photo-1558171813-4c088753af8f?w=600",
                        "https://images.unsplash.com/photo-1596462502278-27bfdd403348?w=600"
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
            
            for p in products:
                db.add(Product(**p))
            db.commit()
            print(f"✅ Seeded {len(products)} products.")
        else:
            print(f"ℹ️ Products already exist – skipping seed.")
            
    except Exception as e:
        db.rollback()
        print(f"❌ Error during seeding: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
    print("Seed script finished.")
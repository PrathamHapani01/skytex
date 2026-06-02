from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:admin@db:5432/skytex")

# Neon requires SSL mode; detect automatically
connect_args = {}
if "neon.tech" in DATABASE_URL or "sslmode" in DATABASE_URL:
    connect_args = {"sslmode": "require"}

# Connection pool tuned for Neon's serverless architecture:
#   - pool_pre_ping: detect stale connections (Neon may close idle ones)
#   - pool_size: keep small to stay within Neon's connection limits
#   - max_overflow: allow a few extra connections during traffic spikes
#   - pool_recycle: recycle connections every 5 minutes to avoid timeouts
engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
    pool_recycle=300,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

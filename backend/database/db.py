from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from backend.config import DATABASE_URL
from loguru import logger

# ================================
# DATABASE ENGINE
# ================================

try:
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
    logger.info("Database engine created successfully")

except Exception as e:
    logger.error(f"Database engine creation failed: {e}")
    raise

# ================================
# SESSION FACTORY
# ================================

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# ================================
# BASE MODEL
# ================================

Base = declarative_base()

# ================================
# DEPENDENCY FOR FASTAPI
# ================================

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
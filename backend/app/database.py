import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# 1. Membaca file .env
load_dotenv()

# 2. Mengambil URL database dari environment variable
DATABASE_URL = os.getenv("DATABASE_URL")

# 3. Membuat engine koneksi SQLAlchemy
engine = create_engine(DATABASE_URL)

# 4. Membuat session factory untuk transaksi query
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 5. Base class yang nantinya diwarisi oleh model tabel
Base = declarative_base()

# 6. Dependency generator untuk membuka dan menutup koneksi tiap ada request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
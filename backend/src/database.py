#!/usr/bin/env python3
"""
Database schema and connection
"""
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Database URL - change this if using Supabase
DATABASE_URL = "postgresql://cloudsaver:devpassword123@localhost:5432/cloudsaver"
# For Supabase, use: DATABASE_URL = "postgresql://postgres:[YOUR-PASSWORD]@..."

# Create engine
engine = create_engine(DATABASE_URL)

# Create session maker
SessionLocal = sessionmaker(bind=engine)

# Base class for models
Base = declarative_base()

# Define Cost table
class CostRecord(Base):
    __tablename__ = "cost_records"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, index=True)
    service = Column(String, nullable=False, index=True)
    cost = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<CostRecord(date={self.date}, service={self.service}, cost=${self.cost})>"

# Create tables
def init_db():
    """Create all tables"""
    Base.metadata.create_all(bind=engine)
    print("✓ Database tables created")

if __name__ == "__main__":
    print("Creating database tables...")
    init_db()
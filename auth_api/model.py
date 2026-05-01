from sqlalchemy import Column, Integer, String
from logindb import Base

class Login(Base):
    __tablename__ = "login"

    id = Column(Integer, primary_key=True, index=True)  # ✅ REQUIRED
    username = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)

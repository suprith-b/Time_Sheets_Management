from sqlalchemy import Column, ForeignKey, Integer, String

from app.db.database import Base


class Password(Base):
    __tablename__ = "passwords"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    username = Column(String(50), unique=True)
    password = Column(String(60))

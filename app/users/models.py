from sqlalchemy import Boolean, Column, ForeignKey, Integer, String,DateTime
from project.database import Base
import datetime as _dt
import sqlalchemy.orm as _orm
import passlib.hash as _hash




class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    date_created = Column(DateTime, default=_dt.datetime.utcnow)

    posts = _orm.relationship("Post", back_populates="owner")

    def verify_password(self, password: str):
        return _hash.bcrypt.verify(password, self.hashed_password)

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    post_text = Column(String, index=True)
    date_created = Column(DateTime, default=_dt.datetime.utcnow)

    owner = _orm.relationship("User", back_populates="posts")


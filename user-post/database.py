from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, text, ForeignKey
# from sqlalchemy.sql.expression import text
# from sqlalchemy.sql.sqltypes import TIMESTAMP


SQLALCHEMY_DATABASE_URL = "sqlite:///tweet.db"


engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db    
    finally:
        db.close()

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, default=True, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text('CURRENT_TIMESTAMP')
    )

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique = True)
    password = Column(String, nullable=False)

    posts = relationship("Post", backref="User", cascade="all, delete-orphan")


    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text('CURRENT_TIMESTAMP')
    )
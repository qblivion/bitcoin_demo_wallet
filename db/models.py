# models.py
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float

Base = declarative_base()

class Account(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    address = Column(String, unique=True, nullable=False)
    private_key = Column(String, nullable=False)
    balance = Column(Float, default=0.0)
    public_key = Column(String, nullable=False)


class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    sender_address = Column(String, nullable=False)
    recipient_address = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    transaction_hash = Column(String, unique=True, nullable=False)
    signature = Column(String, nullable=False)

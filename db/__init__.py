# init.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base
import logging

# Устанавливаем уровень логирования для SQLAlchemy на WARNING, чтобы видеть только предупреждения и ошибки
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.ERROR)

def init_db(db_url='sqlite:///bitcoin_wallet.db'):
    engine = create_engine(db_url, echo=False)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)

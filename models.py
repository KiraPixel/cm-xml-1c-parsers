from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, JSON, ForeignKey, Float, Boolean, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import config

Base = declarative_base()


class Transport(Base):
    __tablename__ = 'transport'
    id = Column(Integer, primary_key=True)
    storage_id = Column(Integer, nullable=False)
    model_id = Column(Integer, nullable=False)
    vin = Column(Text)
    manufacture_year = Column(Text)
    uNumber = Column(Text)
    x = Column(Float, default=0)
    y = Column(Float, default=0)
    customer = Column(Text)
    manager = Column(Text)
    alert_preset = Column(Integer, default=0)
    parser_1c = Column(Integer, default=0)


class Storage(Base):
    __tablename__ = 'storage'

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    type = Column(String(100))
    region = Column(String(100))
    address = Column(String(100))
    organization = Column(String(100))


class TransportModel(Base):
    __tablename__ = 'transport_model'

    id = Column(Text, primary_key=True)
    type = Column(String(100))
    name = Column(String(100))
    lift_type = Column(String(100))
    engine = Column(String(100))
    country = Column(String(100))


class ParserTasks(Base):
    __tablename__ = 'tasks_parser'

    id = Column(Integer, primary_key=True)
    task_name = Column(String(100))
    info = Column(String(100))
    variable = Column(String(100))
    task_completed = Column(Integer, default=0)
    task_manager = Column(String, default='xml_parser')


class TransferTasks(Base):
    __tablename__ = 'tasks_transport_transfer'

    id = Column(Integer, primary_key=True)
    uNumber = Column(String(100))
    old_storage = Column(Integer())
    new_storage = Column(Integer())
    old_manager = Column(String(100))
    new_manager = Column(String(100))
    old_client = Column(String(100))
    new_client = Column(String(100))
    date = Column(Integer())


def get_engine():
    """Возвращает объект engine для базы данных"""
    return create_engine(config.SQLALCHEMY_DATABASE_URL)


def create_db():
    """Создает базу данных и таблицы"""
    engine = get_engine()
    Base.metadata.create_all(engine)
    return engine


def create_session(engine):
    """Создает и возвращает сессию"""
    Session = sessionmaker(bind=engine)
    return Session()

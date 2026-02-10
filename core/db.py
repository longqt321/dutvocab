from datetime import date

from sqlmodel import Session, SQLModel, create_engine, select

from .models import Card

DB_NAME = "./database/dutvocab.db"
engine = create_engine(f"sqlite:///{DB_NAME}", connect_args={"check_same_thread": False})

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    return Session(engine)

def get_all_cards():
    with get_session() as s:
        stmt =  select(Card)
        return s.exec(stmt).all()

def get_due_cards():
    with get_session() as s:
        today = date.today()
        stmt = select(Card).where(Card.next_review <= today)
        return s.exec(stmt).all()

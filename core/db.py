from datetime import date
from typing import Any

import polars as pl
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

def add_card(word: str,
             meaning: str,
             level: str = None,
             note: str = None) -> tuple[bool,str]:
    with get_session() as s:
        stmt = select(Card).where(Card.word == word)
        existing = s.exec(stmt).first()
        if existing:
            return False,f"{word} existed in database."
        new_card = Card(word=word,
                        meaning=meaning,
                        level=level,
                        note=note)
        s.add(new_card)
        s.commit()
        return True,f"Import {word} successfully"

def import_from_csv(df: pl.DataFrame) -> dict[str,Any]:
    report = {
        "success_count": 0,
        "skip_count": 0,
        "errors": []
    }
    with get_session() as s:
        existing_words = set(s.exec(select(Card.word)).all())
        
        for row in df.iter_rows(named=True):
            word = str(row.get('word','')).strip()
            meaning = str(row.get('meaning','')).strip()

            if not word or not meaning:
                continue
            if word in existing_words:
                report["skip_count"] +=1
                continue
            
            level_val = row.get('level')
            note_val = row.get('note')

            level = str(level_val) if level_val is not None else None
            note = str(note_val) if note_val is not None else None

            try:
                new_card = Card(
                    word=word,
                    meaning=meaning,
                    level=level,
                    note=note
                )
                s.add(new_card)
                report["success_count"] += 1
                existing_words.add(word)
            except Exception as e:
                report["errors"].append(f"{word}: {str(e)}")
        s.commit()
    return report

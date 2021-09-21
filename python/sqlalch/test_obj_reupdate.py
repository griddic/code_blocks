import os
import sqlite3

from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

PATH = "mydatabase.db"

engine = create_engine(f'sqlite:///{PATH}', echo=True)
Base = declarative_base()

class Albums(Base):
    __tablename__ = 'albums'
    # id = Column('id', String, primary_key=True, autoincrement=True)
    title = Column('title', String, primary_key=True)
    artist = Column('artist', String)
    publisher = Column('publisher', String)

    def __str__(self):
        return f"{self.title=};{self.artist=};{self.publisher=}"

def recreate_base():
    if os.path.exists(PATH):
        os.remove(PATH)
    conn = sqlite3.connect(PATH)  # или :memory: чтобы сохранить в RAM
    cursor = conn.cursor()

    # Создание таблицы
    cursor.execute("""CREATE TABLE albums
                          (title text, artist text, release_date text,
                           publisher text, media_type text)
                       """)

    cursor.execute("""INSERT INTO albums
                          VALUES ('Glow', 'Andy Hunter', '7/24/2012',
                          'Xplore Records', 'MP3')"""
                   )

    # Сохраняем изменения
    conn.commit()
    conn.close()

if __name__ == '__main__':
    recreate_base()

    ss = sessionmaker(bind=engine, autocommit=True)
    with ss() as session:
        session: Session
        alb: Albums = session.query(Albums).first()
        print(alb)
        with session.begin():
            alb.artist = 'griddic'

        print(alb)

        with session.begin():
            alb.publisher = 'griddic'

        print(alb)




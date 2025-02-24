import os
from sqlalchemy import create_engine, Column, Integer, String, JSON, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

# Подключение к базе данных
DB_HOST = os.getenv('FSTR_DB_HOST')
DB_PORT = os.getenv('FSTR_DB_PORT')
DB_LOGIN = os.getenv('FSTR_DB_LOGIN')
DB_PASS = os.getenv('FSTR_DB_PASS')
DB_NAME = os.getenv('FSTR_DB_NAME')

DATABASE_URL = f"postgresql://{DB_LOGIN}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Модель для таблицы pereval_added
class PerevalAdded(Base):
    __tablename__ = 'pereval_added'
    id = Column(Integer, primary_key=True, autoincrement=True)
    date_added = Column(String)
    raw_data = Column(JSON)
    images = Column(JSON)
    status = Column(String, default='new', nullable=False)

    __table_args__ = (
        CheckConstraint(status.in_(['new', 'pending', 'accepted', 'rejected']), name='status_check'),
    )

# Создание таблиц в базе данных
Base.metadata.create_all(bind=engine)

# Класс для работы с базой данных
class Database:
    def __init__(self):
        self.session = SessionLocal()

    def add_pereval(self, data):
        pereval = PerevalAdded(**data)
        self.session.add(pereval)
        self.session.commit()
        return pereval.id

    def get_pereval_by_id(self, id):
        return self.session.query(PerevalAdded).filter(PerevalAdded.id == id).first()

    def update_pereval(self, id, data):
        pereval = self.get_pereval_by_id(id)
        if not pereval:
            return None
        for key, value in data.items():
            setattr(pereval, key, value)
        self.session.commit()
        return pereval

    def get_pereval_by_email(self, email):
        return self.session.query(PerevalAdded).filter(
            PerevalAdded.raw_data["user_email"].astext == email
        ).all()

    def close(self):
        self.session.close()
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, BigInteger
from sqlalchemy.orm import mapped_column, Mapped

Base = declarative_base()

class UserValuesModel(Base):
    __tablename__ = 'users_values'

    telegram_id: BigInteger = Column("telegram_id", BigInteger, primary_key=True)
    values: Mapped[str] = mapped_column("values", String, nullable=False)

    def __init__(self, telegram_id, values):
        self.telegram_id = telegram_id
        self.values = values

    def __repr__(self):
        return str(self.values)
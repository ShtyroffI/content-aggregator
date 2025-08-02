from sqlalchemy import BigInteger, String, ForeignKey, Integer
from sqlalchemy.orm import declarative_base, Mapped, mapped_column

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str] = mapped_column(String(32), nullable=True)
    first_name: Mapped[str] = mapped_column(String(64))

class Subscription(Base):
    __tablename__ = 'subscriptions'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.user_id'))
    keyword: Mapped[str] = mapped_column(String(100))
    
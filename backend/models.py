from sqlalchemy import String, Integer, Column
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from sqlalchemy.ext.hybrid import hybrid_property
from passlib.context import CryptContext

Base = declarative_base()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30), index=True)
    mail: Mapped[str] = mapped_column(String(105), unique=True, index=True)
    _password_hash: Mapped[str] = mapped_column(String(128))
    role: Mapped[str] = mapped_column(default="user")

    @hybrid_property
    def password(self):
        return '********'
    
    @password.setter
    def password(self, plain_password):
        self._password_hash = pwd_context.hash(plain_password)

    def verify_password(self, plain_password):
        return pwd_context.verify(plain_password, self._password_hash)

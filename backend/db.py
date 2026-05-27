from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session

Base = declarative_base()

engine = create_engine("sqlite:///./sql_app.db", echo=True)

Session = sessionmaker(bind=engine)

with Session() as session:
    results = session.query(User).all()

async def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()



from database import *

from sqlalchemy import *

class User(Base):
    __tablename__ = 'user'
    age = Column(Integer)
    city = Column(String)
    country = Column(String)
    exp_group = Column(Integer)
    gender = Column(Integer)
    id = Column(Integer, primary_key=True)
    os = Column(String)
    source = Column(String)


if __name__ == "__main__":
    session = SessionLocal()
   # result = list()
    print (
        session.query(User.country, User.os, func.count("*"))
        .filter(User.exp_group == 3)
        .group_by(User.country, User.os)
        .having(func.count("*") > 100)
        .order_by(func.count("*").desc())
        .all()
    )
       # result.append(i.id)
    print(result)
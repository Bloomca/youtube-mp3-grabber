from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Subscription(Base):
    __tablename__ = 'subscriptions'

    id = Column(Integer, primary_key=True)
    channel = Column(String(250), nullable=False)
    name = Column(String(1000), nullable=False)
    fetchedBefore = Column(String(1000), nullable=False)

engine = create_engine('sqlite:///youtube-grabber.db')

Base.metadata.create_all(engine)
 
import os
import logging

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

# Database struct
Base = declarative_base()
class Fact(Base):
    __tablename__ = "facts"
    
    id = Column(Integer, primary_key=True)
    content = Column(String)
    
    preview_links = relationship("PreviewLink", back_populates="fact")
    featured_image = relationship("FeaturedImage", uselist=False, back_populates="fact")

class PreviewLink(Base):
    __tablename__ = "preview_links"
    
    id = Column(Integer, primary_key=True)
    url = Column(String)
    
    fact_id = Column(Integer, ForeignKey("facts.id"))
    fact = relationship("Fact", back_populates="preview_links")

class FeaturedImage(Base):
    __tablename__ = "featured_images"
    
    id = Column(Integer, primary_key=True)
    image_url = Column(String)
    caption = Column(String)
    
    fact_id = Column(Integer, ForeignKey("facts.id"))
    fact = relationship("Fact", back_populates="featured_image")

def create_engine(path: string):
    # Create the database engine and session
    database_file = "wiki_data.db"
    if os.path.isfile(database_file):
        logging.info("Database already exists")
        engine = create_engine(f"sqlite:///{database_file}")
        return engine
    else:
        # Create the tables if the database doesn't exist
        Base.metadata.create_all(engine)
        logging.info('Database created.')
        return engine

def create_session(engine):
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

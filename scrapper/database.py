from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from datetime import datetime

Base = declarative_base()

class Fact(Base):
    __tablename__ = "facts"

    id = Column(Integer, primary_key=True)
    content = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    day_of_week = Column(String)
    analyzed = Column(Boolean, default=False)
    internal_links = Column(String)
    campaign_parameters = Column(String)

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

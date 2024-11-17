from sqlalchemy import Column, BigInteger, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone

Base = declarative_base()

class JobPostModel(Base):
    __tablename__ = 'job_posts'

    title = Column(String, nullable=False)
    url = Column(String, nullable=False)

    def __repr__(self):
        return f"<Job(title={self.title}, url={self.url})>"
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import Column, String, DateTime, func

class TimeStampModelMixin:
    id = Column(String,primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower() + "s"  # autogenerate table_name

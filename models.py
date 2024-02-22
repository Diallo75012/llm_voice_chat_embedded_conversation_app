import uuid
from sqlalchemy import create_engine, Column, Integer, ForeignKey, String, Table, ARRAY, Float, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

metadata = MetaData()
Base = declarative_base()

class PgRecord(Base):
    __tablename__ = 'pgrecord'
    id_nbr = Column(Integer, primary_key=True) #will be unique and will autoincrement natively
    embedding_id = Column(Integer, nullable=True)

class ConversationEmbedding(Base):
    __tablename__ = 'conversation_embedding'  # Table name
    id = Column(Integer, primary_key=True)
    unique_identifier = Column(UUID(as_uuid=True), nullable=False)
    data_vector = Column(ARRAY(Float))
    other_data = Column(String)

# from sqlalchemy.dialects.postgresql import ARRAY
# Column("data", ARRAY(Integer, dimensions=1024))
# Column("data", ARRAY(Float))

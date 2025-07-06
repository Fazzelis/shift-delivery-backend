from sqlalchemy import Column, Integer, String, ForeignKey, Time, Date, func, Table, Boolean
from database.database_conf import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "user"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, server_default=func.gen_random_uuid())
    phone_number = Column(String, unique=True)
    email = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    middle_name = Column(String)
    password_hash = Column(String)
    orders = relationship("Order", back_populates="user")
    city_id = Column(UUID(as_uuid=True), ForeignKey("city.id"))
    city = relationship("City", back_populates="users")


class City(Base):
    __tablename__ = "city"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, server_default=func.gen_random_uuid())
    name = Column(String, unique=True)
    lat = Column(String)
    lon = Column(String)
    users = relationship("User", back_populates="city")


class Package(Base):
    __tablename__ = "package"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, server_default=func.gen_random_uuid())
    name = Column(String)
    length = Column(Integer)# см
    width = Column(Integer)# см
    height = Column(Integer)# см
    icon_id = Column(UUID)


class Attachment(Base):
    __tablename__ = "attachment"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, server_default=func.gen_random_uuid())
    path = Column(String, unique=True)


class Order(Base):
    __tablename__ = "order"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, server_default=func.gen_random_uuid())
    delivery_type = Column(Boolean)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))
    user = relationship("User", back_populates="orders")
    to_surname = Column(String)
    to_name = Column(String)
    to_middle_name = Column(String)
    to_email = Column(String)

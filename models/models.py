from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import Column, Integer, String, ForeignKey, MetaData, Table, UniqueConstraint, Boolean
from sqlalchemy.ext.asyncio import AsyncAttrs


# from flask_image_alchemy.utils import
# storage = S3


class Base(AsyncAttrs, DeclarativeBase):
    pass


# class User(Base):
#     __tablename__ = 'users'
#
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     tg_id = Column(Integer, nullable=True)
#     name = Column(String, nullable=True)
#
#
class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True, autoincrement=True)
    tg_id = Column(Integer, nullable=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    city = Column(String, nullable=True)
    addresses_street = Column(String, nullable=True)
    addresses_home = Column(String, nullable=True)
    addresses_comment = Column(String, nullable=True)
    phone = Column(String, nullable=False)
    is_active = Column(Boolean, default=False)
#
#
class CategoryProduct(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    company = Column(Integer, ForeignKey('companies.id'))
#
#
ingredients_product = Table('ingredients_product', Base.metadata,
                            Column('product_id', Integer(), ForeignKey('products.id')),
                            Column('ingredient_id', Integer(), ForeignKey('ingredients.id'))
                            )
#
#
class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    url_picture = Column(String, nullable=False)
    price = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    category = Column(Integer, ForeignKey('categories.id'))
    weight = Column(String, nullable=True)
    ingredient = relationship("Ingredient", secondary=ingredients_product, backref="products")



class Ingredient(Base):
    __tablename__ = 'ingredients'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    availability = Column(Boolean, default=True)


# class Image(Base):
#     __tablename__ = 'images'
#
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     name = Column(String)
#     url = Column(String)

# order_products = Table('orders_products', Base.metadata,
#                             Column('product_id', Integer(), ForeignKey('products.id')),
#                             Column('ingredient_id', Integer(), ForeignKey('ingredients.id'))
#                             )
#
# class Order(Base):
#     __tablename__ = 'orders'
#
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     user_id = Column(Integer, ForeignKey('users.id'))
#     total_price = Column(Integer, nullable=False)
#     status = Column(String, nullable=False)
#     products = relationship('OrderProduct')


async def create_all_tables(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)



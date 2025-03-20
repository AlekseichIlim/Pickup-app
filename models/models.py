from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, ForeignKey, MetaData, Table, UniqueConstraint, Boolean

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    tg_id = Column(Integer, nullable=True)
    name = Column(String, nullable=True)


class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True, autoincrement=True)
    tg_id = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    city = Column(String, nullable=True)
    addresses_street = Column(String, nullable=True)
    addresses_home = Column(String, nullable=True)
    addresses_comment = Column(String, nullable=True)
    phone = Column(Integer, nullable=False)


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    company = Column(Integer, ForeignKey('companies.id'))
    products = relationship('Product')


ingredients_product = Table('ingredients_product', Base.metadata,
                            Column('product_id', Integer(), ForeignKey('products.id')),
                            Column('ingredient_id', Integer(), ForeignKey('ingredients.id'))
                            )




class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    # picture = Column(String, nullable=False)
    price = Column(Integer, nullable=True)
    active = Column(Boolean, default=True)
    category = Column(Integer, ForeignKey('categories.id'))
    ingredient = relationship("Ingredient", secondary=ingredients_product, backref="products")


class Ingredient(Base):
    __tablename__ = 'ingredients'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    availability = Column(Boolean, default=True)



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
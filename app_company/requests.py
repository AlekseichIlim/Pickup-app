import asyncio

from sqlalchemy import select

from config import AsyncSessionLocal
from models.models import Company, Product, CategoryProduct
from sqlalchemy.exc import IntegrityError


# def save_data_problem(object, session):
#     """Заполнение данных продукта"""
#
#     try:
#         new_problem = Product(
#             contest_id=problem.contest_id,
#             index=problem.index,
#             name=problem.name,
#             tags=', '.join(problem.tags),
#             rating=problem.rating,
#             solved_count=problem.solved_count
#         )
#         session.add(new_problem)
#         session.commit()
#     except IntegrityError:
#         session.rollback()
#         continue
#
#     session.close()

async def save_data_company(data):
    """Заполнение данных компании"""

    try:
        new_company = Company(
            name=data['name'],
            description=data['description'],
            city=data['city'],
            addresses_street=data['addresses_street'],
            addresses_home=data['addresses_home'],
            addresses_comment=data['addresses_comment'],
            phone=data['phone'],
            is_active=True
        )
        async with AsyncSessionLocal() as session:
            session.add(new_company)
            await session.commit()
    except IntegrityError:
        await session.rollback()


async def save_data_category(data_category, data_company):
    """Заполнение данных категории"""

    try:
        new_category = CategoryProduct(
            name=data_category['name_category'],
            company=int(data_company['id'])
        )
        async with AsyncSessionLocal() as session:
            session.add(new_category)
            await session.commit()
    except IntegrityError:
        await session.rollback()


async def get_categories(data_company):
    async with AsyncSessionLocal() as session:
        categories = session.query(CategoryProduct).filter(CategoryProduct.company == data_company['id']).all()
    if categories:
        return categories
    else:
        return None


async def get_all_objects(model):
    """ Возвращает все объекты модели """

    async with AsyncSessionLocal() as session:
        result = await session.execute(select(model))
        return result.scalars().all()


async def get_one_object(model, obj_id):
    """ Возвращает объект модели """

    async with AsyncSessionLocal() as session:
        obj = select(model).where(model.id == obj_id)
        result = await session.execute(obj)
        return result.scalar_one_or_none()


async def get_all_objects_foreignkey(primary_class_and_field, item_field):
    """ Возвращает объекты класса по указанному вторичному ключу
    primary_class_and_field - класс с указанием поля: Product.category
    item_field - значение вторичного ключа: int
    """
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(primary_class_and_field).where(primary_class_and_field == item_field))
        return result.scalars().all()

data = {
    'name': 'Шаурма 1', 'description': '', 'city': 'Усть-Илимск', 'addresses_street': 'Мира', 'addresses_home': '40',
    'addresses_comment': 'у рынка', 'phone': 60045
}

# res = asyncio.run(get_all_objects_foreignkey(CategoryProduct.company, 2))

# res = asyncio.run(get_one_object(Company, 2))
# print(res)
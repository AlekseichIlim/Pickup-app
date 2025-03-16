from models.models import Base


def main(engine):

    # Создание всех таблиц в базе данных
    Base.metadata.create_all(engine)

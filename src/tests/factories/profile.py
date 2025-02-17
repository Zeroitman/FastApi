import factory
from async_factory_boy.factory.sqlalchemy import AsyncSQLAlchemyFactory
from tests.conftest import TestSessionLocal
from backend.authentication import hashed_password
from backend.db.models import Profile


class ProfileFactory(AsyncSQLAlchemyFactory):
    email = factory.Faker('email')
    password = hashed_password('1qaz@WSX29')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    phone = factory.Sequence(lambda x: "99655533667{}".format(x))

    class Meta:
        model = Profile
        sqlalchemy_session = TestSessionLocal
        sqlalchemy_session_persistence = 'commit'

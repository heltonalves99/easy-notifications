from bottle.ext import sqlalchemy
from models import Base, engine, test_engine


def sql_plugin(test=False):
    return sqlalchemy.Plugin(
        engine if test else test_engine,
        Base.metadata,
        keyword='db',
        create=False,
        commit=True,
        use_kwargs=False
    )

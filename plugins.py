from bottle.ext import sqlalchemy
from models import Base, engine


sqlplugin = sqlalchemy.Plugin(
    engine,
    Base.metadata,
    keyword='db',
    create=False,
    commit=True,
    use_kwargs=False
)

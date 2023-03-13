from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_repr import RepresentableBase


Model = declarative_base(name="Model", cls=RepresentableBase)
metadata = Model.metadata

from sqlalchemy.exc import ArgumentError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_repr import RepresentableBase


class Model(RepresentableBase):
    def update(self, **kwargs):
        model_columns = {column.name for column in self.__table__.columns}
        update_columns = set(kwargs)
        if not update_columns.issubset(model_columns):
            raise ArgumentError(
                f"Unsupported fields received: {update_columns - model_columns}. "
            )
        for key, value in kwargs.items():
            setattr(self, key, value)


Model = declarative_base(name="Model", cls=Model)


metadata = Model.metadata

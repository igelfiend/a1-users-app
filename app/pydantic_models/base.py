from pydantic import BaseModel, Extra


class NoExtraFieldsModel(BaseModel):
    class Config:
        extra = Extra.forbid

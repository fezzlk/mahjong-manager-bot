from sqlalchemy import Column, String, Integer
from setting import BaseModel


class UserModel(BaseModel):
    """
    UserModel
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)

    def __init__(self, name):
        self.name = name

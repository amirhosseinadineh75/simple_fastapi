from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Float, engine, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base, engine

import datetime

import sqlalchemy.types as types

class ChoiceType(types.TypeDecorator):

    impl = types.String

    def __init__(self, choices, **kw):
        self.choices = dict(choices)
        super(ChoiceType, self).__init__(**kw)

    def process_bind_param(self, value, dialect):
        return [k for k, v in self.choices.iteritems() if v == value][0]

    def process_result_value(self, value, dialect):
        return self.choices[value]

class AccountTable(Base):
   __tablename__ = "accounts"   

   id              = Column(Integer, 
                            primary_key = True, 
                            index       = True)
   shaba           = Column(String, unique = True)
   card            = Column(String, unique = True)
   number          = Column(String, unique = True)
   bank            = Column(String)
   created_at      = Column(DateTime, default = datetime.datetime.utcnow)

   status          = Column(
      ChoiceType({
         "buy"    : "buy", 
         "sell"   : "sell", 
         "wallet" : "wallet",
         "other"  : "other"}), 
      nullable = False )

Base.metadata.create_all(bind=engine)

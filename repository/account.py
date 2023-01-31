

# from .services          import getEn
from models.models    import AccountTable
from models.database import QueryDbClass
# from .decorators        import *
from massages.global_massage import *

import datetime

HARD_DELETE_DAYS = 30

class Account():
   def __init__(self):
      print("Account  constructor")
      # self.ormDb         = AccountTable()
      self.db            = QueryDbClass()
      self.status_fa      = [
         'حساب فروش',  'حساب  خرید',
         'کیف پول',     'سایر'  ]

      self.status_en      = [
         'buy',    'sell',
         'wallet', 'other'
      ]
           

      self.class_name = self.__class__.__name__ 

   def prepareListData(self, ids):
      res = []
      for id in ids:
         temp_value = self.get_one(id[0])
         if temp_value != []:
               res.append(temp_value)
      return res

   def prepareData(self, rows, is_admin = False):
      res = []
      for row in rows:
         # if row[9] is None or is_admin:
               res.append({
                  "id"     : row[0], "shaba" : row[1], "card"       : row[2],
                  "number" : row[3], "bank"  : row[4], "created_at" : row[5]
               })
      return res

   def get_types(self):
      return self.status_fa

   def get_one(self,
               id, 
               is_update_cache = False,
               is_delete_cache = False,
               is_admin        = False):
      self.db.checkDbConnection()
      self.db.cursor.execute('''
         select * from accounts
         where id = %s
      ''', (id, ))
      data = self.prepareData(self.db.cursor.fetchall(), is_admin = is_admin)
      if data != []:
         return data[0]
      return data

   def get_all_query(self, limit, offset,
                     is_update_cache = False,
                     is_delete_cache = False):
      self.db.checkDbConnection()
      self.db.cursor.execute('''
         select id from accounts 
            limit %s offset %s
      ''', (limit, offset))
      return self.db.cursor.fetchall()

   def get_all(self, limit, offset,
               is_update_cache = False,
               is_delete_cache = False):
      ids = self.get_all_query(limit, 
                              offset, 
                              is_update_cache, 
                              is_delete_cache)
      return self.prepareListData(ids)
    
   def get_by_type_query(self, type,
                  is_update_cache = False,
                  is_delete_cache = False):
      self.db.checkDbConnection()
      self.db.cursor.execute('''
         select id from accounts 
         where status = %s
      ''', (type, ))
      return self.db.cursor.fetchall()

   def get_by_type(self, type,
                  is_update_cache = False,
                  is_delete_cache = False):
      ids = self.get_by_type_query(type)
      return self.prepareListData(self.db.cursor.fetchall())


   def add(self, arg, OPERATOR = ''):
      self.db.checkDbConnection()
      self.db.cursor.execute('''
      insert into accounts
      (
         number, card,     shaba,
         bank,   status,   created_at
      )
      values
      (
         %s, %s, %s,
         %s, %s, now()
      ) RETURNING id;
      ''',(
         arg["number"]  , arg["card"]   , arg["shaba"]  ,
         arg["bank"]    , 'sell'
      ))
      self.db.connection.commit()
      id = self.db.cursor.fetchone()
      if not id :
         return False, None
      id = id[0]
      return True, self.get_one(id)

   def hard_delete(self, id, OPERATOR = ''):
      self.db.checkDbConnection()
      self.db.cursor.execute('''
      delete from accounts 
      where id = %s and
      CURRENT_DATE - date(deleted_at) >= %s
      ''',(id, HARD_DELETE_DAYS))
      self.db.connection.commit()
      self.get_one(id, is_delete_cache = True)
      return True

   def update(self, arg, id = '', OPERATOR = ''):
      self.db.checkDbConnection()
      self.db.cursor.execute('''
      update accounts set
         number  = %s , card  = %s, 
         shaba   = %s,  bank  = %s 
      where id = %s
      ''',(
         arg["number"],  arg["card"],
         arg["shaba"],   arg["bank"],
         id
      ))
      self.db.connection.commit()
      self.get_one(id, is_update_cache = True)
      return True


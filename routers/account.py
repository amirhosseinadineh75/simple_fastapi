from fastapi                 import APIRouter, HTTPException, Request
from repository.account      import Account
from massages.global_massage import *
from schemas.account_items   import AccountItem

account_router = APIRouter(
    tags    = ['Account'],
    prefix  = "/account"
)


@account_router.get("/" , summary = INFO_GET_BY_ID)
def get_one(id : int):
    obj       = Account()
    rows      = obj.get_one(id)
    return {"data": rows}

@account_router.get("/all", summary = INFO_GET_BY_ALL_WITH_PAGGINATION)
def get_all(limit : int = 10,
            page  : int = 1):
    obj       = Account()
    rows      = obj.get_all(limit, page - 1)
    return {"data": rows}

@account_router.post('/', summary = INFO_INSERT)
def add(item: AccountItem):
    obj          = Account()
    item         = item.dict()
    flag, data   = obj.add(item, OPERATOR = 'username')
    if not flag:
      if data is None:
         raise HTTPException(status_code = 400,
                              detail      = ERROR_DONT_INSERT)
      else:
         raise HTTPException(status_code = 400,
                     detail      = data)
    return {"result": flag, "data" : data}

@account_router.put('/')
def update(id   : int,
           item : AccountItem):
    obj   = Account()
    item  = item.dict()
    flag  = obj.update(item, id = id, OPERATOR = 'username')
    return {"result": flag}

@account_router.delete("/hard", summary = INFO_HARD_DELETE)
def hard(id: str):
    obj   = Account()
    flag  = obj.hard_delete(id, OPERATOR = 'username')
    return {"result" : flag}





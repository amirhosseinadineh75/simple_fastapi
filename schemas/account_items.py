
from typing   import Optional, List
from pydantic import BaseModel

class AccountItem(BaseModel):
    number   : str
    card     : str
    shaba    : str
    bank     : str
    # status   : int
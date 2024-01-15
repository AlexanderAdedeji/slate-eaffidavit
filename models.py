from typing import Dict, Any
from typing import Any, Dict
from pydantic import BaseModel
from datetime import datetime



class MongoBase(BaseModel):
    @classmethod
    def __collectionname__(cls):
        return cls.__name__.lower()

class Templates(MongoBase):
    data: Dict[str, Any]

class Documents(MongoBase):
    data: Dict[str, Any]
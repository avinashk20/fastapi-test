from pydantic import BaseModel

class UserData(BaseModel):
    email: str
    phone: str
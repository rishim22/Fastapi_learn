from pydantic import BaseModel, EmailStr    
class UserCreate(BaseModel):#rem: this is a schema for user creation, it defines the expected fields and their types when creating a new user.
    email: EmailStr
    password: str   
    username: str
    role: str = "user"
class UserLogin(BaseModel):#rem: this is a schema for user login, it defines the expected fields and their types when a user attempts to log in.
    email: EmailStr
    password: str   
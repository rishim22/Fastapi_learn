from fastapi import FastAPI,Depends,HTTPException,status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import jwt

from auth_database import get_db
import models
import schemas
import utils


SECRET_KEY = "xELujFcnTqGKoe85_aZrb2mUeUpNwbHef5jMgYJiW_o" #rem: In a production application, this should be a secure, randomly generated key and kept secret.  
ALGORITHM= "HS256" #rem: This is the algorithm used for encoding and decoding JWT tokens. HS256 is a common choice for symmetric encryption.
ACCESS_TOKEN_EXPIRE_MINUTES = 30 #rem: This defines how long the access token will be valid. After this time, the user will need to log in again to get a new token.

#HElper function that takes user data
def create_access_token(data: dict):
    to_encode = data.copy()
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

app = FastAPI()
@app.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered") 
    hashed_password = utils.hash_password(user.password)
    new_user = models.User(email=user.email, hashed_password=hashed_password , username=user.username, role=user.role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully"}
@app.post("/login")
def Login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user or not utils.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_100_CONTINUE, detail="Invalid email or password") 
    access_token = create_access_token(data={"sub": db_user.email, "role": db_user.role })
    return {"access_token": access_token, "token_type": "bearer"} 
    
    
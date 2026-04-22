from fastapi import FastAPI,Depends,HTTPException,status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm  
from jose import JWTError
from auth_database import get_db
import models
import schemas
import utils

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
SECRET_KEY = "xELujFcnTqGKoe85_aZrb2mUeUpNwbHef5jMgYJiW_o" #rem: In a production application, this should be a secure, randomly generated key and kept secret.  
ALGORITHM= "HS256" #rem: This is the algorithm used for encoding and decoding JWT tokens. HS256 is a common choice for symmetric encryption.
ACCESS_TOKEN_EXPIRE_MINUTES = 30 #rem: This defines how long the access token will be valid. After this time, the user will need to log in again to get a new token.

#HElper function that takes user data
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token

app = FastAPI()

@app.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = db.query(models.User).filter(models.User.email == user.email).first()
        if db_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered") 
        hashed_password = utils.hash_password(user.password)
        new_user = models.User(email=user.email, hashed_password=hashed_password, username=user.username, role=user.role)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {"message": "User registered successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
@app.post("/login")
def Login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    try:
        db_user = db.query(models.User).filter(models.User.email == user.email).first()
        if not db_user or not utils.verify_password(user.password, db_user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password") 
        access_token = create_access_token(data={"sub": db_user.email, "role": db_user.role})
        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) 
    
def get_current_user(token: str = Depends(oauth2_scheme)):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = str(payload.get("sub"))
        role = str(payload.get("role"))
        if username is None or role is None:
            raise credential_exception
        return {"username": username, "role": role}
    except JWTError:
        raise credential_exception

@app.get("/protected")
def protected_route(current_user: dict = Depends(get_current_user)):
    return {"message": f"Hello, {current_user['username']}! This is a protected route."}
def required_role(allowed_roles: str):
    def role_checker(current_user: dict = Depends(get_current_user)):
         user_role = current_user.get("role")
         if user_role not in allowed_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to access this resource")
         
         return current_user
    return role_checker     
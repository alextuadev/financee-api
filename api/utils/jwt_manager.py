import os

from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

# Define some constants
SECRET_KEY=os.environ.get("SECRET_KEY", "")
ALGORITHM = "HS256"
#os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", 30)
ACCESS_TOKEN_EXPIRE_MINUTES: float = 30

# Create an instance of the OAuth2PasswordBearer class
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

# Define a function to generate access tokens
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta: 
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Define a function to decode access tokens
def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    return username

# Define a function to verify access tokens
def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("username")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    return True

# Define a function to authenticate users
def authenticate_user(username: str, password: str):
    # Implement your own authentication logic here
    # This could involve checking a database or external API
    # Return True if authentication is successful, False otherwise
    return True

# Define a function to verify user credentials
def verify_user_credentials(username: str, password: str):
    # Implement your own logic to verify the user's credentials here
    # This could involve checking a database or external API
    # Return True if the credentials are valid, False otherwise
    return True

# Define a function to get user information
def get_user_info(username: str):
    # Implement your own logic to get user information here
    # This could involve querying a database or external API
    # Return a dictionary of user information
    return {"username": username, "email": f"{username}@example.com"}

# Define the main JWT manager function
def jwt_manager(token: str = Depends(oauth2_scheme)):
    username = decode_access_token(token)
    user_info = get_user_info(username)
    return user_info
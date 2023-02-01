from jose import JWTError, jwt
from fastapi import FastAPI, Depends, HTTPException, File, UploadFile, Header
import datetime
from pydantic import BaseModel
from passlib.context import CryptContext
from typing import Union
import secrets

JWT_SECRET = "secret"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = secrets.token_hex(32)
ALGORITHM = "HS256"


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def generate_token(data: dict):
    access_token = jwt.encode(
        data,
        SECRET_KEY,
        algorithm=ALGORITHM

    )
    return access_token


def secure(token):
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        return decoded_token
    except JWTError:
        raise HTTPException(status_code=400, detail="Could not validate credentials")

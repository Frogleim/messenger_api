import datetime
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends, HTTPException, File, UploadFile, Header
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import BaseModel
import secrets
from core import users_db
import base64
from core import avatar_resize
from auth import secure, verify_password, generate_token

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users_db.retrieve_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid username or password")

    access_token = generate_token({'sub': user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/register")
async def register(username: str, password: str):
    check_user = users_db.check_username(username)
    if check_user:
        raise HTTPException(status_code=400, detail="Username already exist")

    users_db.save_users(username, password)
    return {"Message": "Sign Up Successfully"}


@app.post("/change_info")
async def change_info(email: str, auth: str = Header(None), file: UploadFile = File(...)):
    extension = file.filename.split(".")[-1] in ("jpg", "jpeg", "png")
    if not extension:
        raise HTTPException(status_code=400, detail="Image must be jpg or png format!")
    if auth is None:
        raise HTTPException(status_code=422, detail="Unauthorized")
    username = secure(auth)
    user_id = username["sub"]
    image = await file.read()
    resized_image_50 = avatar_resize.resize_image_50(image)
    avatar_50 = base64.b64encode(resized_image_50).decode("utf-8")
    resized_image_100 = avatar_resize.resize_image_100(image)
    avatar_100 = base64.b64encode(resized_image_100).decode("utf-8")
    resized_image_400 = avatar_resize.resize_image_400(image)
    avatar_400 = base64.b64encode(resized_image_400).decode("utf-8")
    users_db.edit_user(user_id, email, avatar_50, avatar_100, avatar_400)
    return {"Message": "Success!"}

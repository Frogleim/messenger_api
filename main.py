from fastapi import FastAPI, Depends, HTTPException, File, UploadFile, Header
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
import secrets
from core import users_db
import base64
from core import avatar_resize

app = FastAPI()

users = {"user1": {"password": "hashed_password1"}, "user2": {"password": "hashed_password2"}}

SECRET_KEY = secrets.token_hex(32)
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=400, detail="Could not validate credentials")


async def auth_user(username: str, password: str):
    user = users_db.check_username(username)
    # user = users.get(username)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    if not password:
        raise HTTPException(status_code=400, detail="Incorrect password")
    return user


def create_access_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


@app.post("/login")
async def login(username: str, password: str):
    user = await auth_user(username, password)
    access_token = create_access_token({"sub": user})
    print(users)
    return {"access token": access_token, "token_type": "bearer"}


@app.post("/signup")
async def signup(username: str, password: str):
    if username in users:
        raise HTTPException(status_code=400, detail="Username already exist")

    users[username] = {"password": password}
    users_db.save_users(username, password)
    return {"message": "User created"}


@app.get("/")
async def root(authorization: str = Header(None)):
    if authorization:
        return {"message": "Authorized"}
    else:
        return {"message": "Not Authorized"}


@app.post("/change_info")
async def change_info(email: str, current_user=Depends(get_current_user), file: UploadFile = File(...)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    extension = file.filename.split(".")[-1] in ("jpg", "jpeg", "png")
    if not extension:
        raise HTTPException(status_code=400, detail="Image must be jpg or png format!")

    username = current_user["sub"]
    user = users.get(username)
    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    image = await file.read()
    resized_image_50 = avatar_resize.resize_image_50(image)  # resize image to 50x50
    avatar_50 = base64.b64encode(resized_image_50).decode("utf-8")
    resized_image_100 = avatar_resize.resize_image_100(image)
    avatar_100 = base64.b64encode(resized_image_100).decode("utf-8")
    resized_image_400 = avatar_resize.resize_image_400(image)
    avatar_400 = base64.b64encode(resized_image_400).decode("utf-8")
    users_db.edit_user(email, avatar_50, avatar_100, avatar_400)
    return {"Message": "Success!"}


@app.get("/protected")
async def protected():
    return {"message": "Welcome to the protected route"}

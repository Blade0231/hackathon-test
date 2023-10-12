from fastapi import FastAPI, HTTPException, Depends, status, Request, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from src.utils import UserDatabase, UserAddress, Schedule, Attendance

from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Optional

from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse

import os

print(os.getcwd())

app = FastAPI()
app.mount("/static", StaticFiles(directory="src/static"), name="static")
templates = Jinja2Templates(directory="src/templates")

SECRET_KEY = "AKATSUKI-NARUTO"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: str or None = None


def create_access_token(data: dict, expires_delta: timedelta or None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: str = Depends(OAuth2PasswordBearer(tokenUrl="/token"))):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    return token_data


class UserLogin(BaseModel):
    user_id: str
    password: str  # You may want to hash and verify the password securely


class UserModel(BaseModel):
    user_id: str
    name: str
    role: str
    phone: str
    email: str
    password: str


class UserAddress(BaseModel):
    user_id: str
    street: str
    city: str
    state: str
    postal_code: str
    country: str


class ScheduleModel(BaseModel):
    user_id: str
    client_id: str
    start_time: datetime
    end_time: datetime


class attendance(BaseModel):
    id_: str
    user_id: str
    status: str


@app.post("/login")
async def login(user_data: UserLogin):
    db = UserDatabase()
    user = db.run_query("SELECT * FROM users WHERE USER_ID = ?", (user_data.user_id,))
    db.close()

    if user.empty:
        raise HTTPException(status_code=401, detail="User not found")

    # You can add password validation logic here if needed
    # For demonstration, we assume the user exists
    if not user_data.password == user.loc[0]["PASSWORD"]:
        raise HTTPException(status_code=401, detail="Incorrect Password")
    # Return a success message (you might want to return a token in a real-world scenario)

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user_data.user_id}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me", response_model=UserLogin)
async def read_users_me(current_user: UserLogin = Depends(get_current_user)):
    return current_user


@app.post("/signup")
async def signup(user_model: UserModel):
    db = UserDatabase()

    try:
        db.add_record(
            user_id=user_model.user_id,
            name=user_model.name,
            role=user_model.role,
            phone=user_model.phone,
            email=user_model.email,
            password=user_model.password,
        )
        db.close()
        return {"message": "User Created"}
    except:
        raise HTTPException(status_code=403, detail="Incorrect Data")


@app.post("/address")
async def add_address(address: UserAddress):
    db = UserAddress()

    try:
        db.add_record(
            user_id=address.user_id,
            street=address.street,
            city=address.street,
            postal_code=address.postal_code,
            country=address.country,
        )
        db.close()
        return {"message": "User Address Updated"}
    except:
        raise HTTPException(status_code=403, detail="Incorrect Data")


@app.post("/create_schedule")
async def create_schedule(schedule: ScheduleModel):
    db = Schedule()

    try:
        db.add_record(
            user_id=schedule.user_id,
            client_id=schedule.client_id,
            start_time=schedule.start_time,
            end_time=schedule.end_time,
        )
        db.close()
        return {"message": "Schedule Created"}
    except:
        raise HTTPException(status_code=403, detail="Incorrect Data")


@app.post("/show_schedule")
async def show_schedule():
    pass


@app.post("/attendance")
async def record_attendance(att: attendance):
    db = Attendance()

    try:
        db.add_record(
            id=att.id_, user_id=att.user_id, status=att.status, created=datetime.now()
        )
        db.close()
        return {"message": "Sucessful"}
    except:
        raise HTTPException(status_code=403, detail="Incorrect Data")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

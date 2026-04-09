from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from pydantic import BaseModel

app = FastAPI()

class TokenInfo(BaseModel):
    username: str
    expires_at: datetime
    is_valid: bool

# Настройки
SECRET_KEY = "secret123"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Хранилище пользователей
users_db = {
    "test": {
        "username": "test",
        # Другой пароль, был сгенерирован с помощью create_hash.py (также test в исходном варианте)
        "password": "$2b$12$4yN7ikL7s/.AbynlJoXvqeBPOHrgbCM8TldgBhUqCg6F5ZQRUfnvy"  # "test"
    }
}

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_token(data: dict):
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data.update({"exp": expire})
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except:
        return None

# ИСПРАВЛЕННЫЙ маршрут - использует OAuth2PasswordRequestForm (исходный код принимал query параметры, а не form-data)
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users_db.get(form_data.username)
    if not user or not pwd_context.verify(form_data.password, user["password"]):
        raise HTTPException(status_code=400, detail="Неверные данные")
    
    token = create_token({"sub": form_data.username})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/secure-data")
async def secure_data(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Недействительный токен")
    
    return {"message": f"Привет, {payload['sub']}! Это защищенные данные."}

@app.get("/token-info")
async def get_token_info(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Недействительный токен")
    
    exp_timestamp = payload.get('exp')
    if exp_timestamp:
        expires_at = datetime.fromtimestamp(exp_timestamp)
        return TokenInfo(
            username=payload['sub'],
            expires_at=expires_at,
            is_valid=expires_at > datetime.now()
        )
    else:
        raise HTTPException(status_code=400, detail="Токен не содержит время истечения")
from jose import jwt, JWTError
from datetime import datetime, timedelta
import config

def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=5)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, config.JWT_SECRET, algorithm=config.JWT_ALGORITHM)

def verify_token(token: str):
    try:
        payload = jwt.decode(token, config.JWT_SECRET, algorithms=[config.JWT_ALGORITHM])
        return payload
    except JWTError:
        return None

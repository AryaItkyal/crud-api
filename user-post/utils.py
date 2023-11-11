from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated='auto') # hashing algo

def hash(password: str):
    return pwd_context.hash(password)

def verify(in_password,  hash_password):
    return pwd_context.verify(in_password,  hash_password)
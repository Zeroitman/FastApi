from passlib.context import CryptContext


# pwd_context stably generates hash of 60 symbols length with this config
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hashed_password(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

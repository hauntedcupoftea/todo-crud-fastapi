from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import JWTError, jwt

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440 # 1 day

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data: dict):
    """
    Generates a JWT access token with a specified expiration time.
    
    :param data: The `data` parameter in the `create_access_token` function is a dictionary containing
    the information that you want to encode into the access token. This data could include things like
    user ID, username, roles, or any other relevant information that you want to include in the token
    :type data: dict
    :return: The function `create_access_token` returns an encoded JSON Web Token (JWT) containing the
    data provided in the `data` dictionary along with an expiration time of 15 minutes from the current
    time.
    """
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token:str, credentials_exception):
    """
    Decodes a JWT token using a secret key and algorithm, extracts the email
    from the payload, and raises a credentials exception if the email is missing or if there is a JWT
    error.
    
    :param token: The `token` parameter is a string that represents a JWT (JSON Web Token) that needs to
    be verified
    :type token: str
    :param credentials_exception: The `credentials_exception` parameter in the `verify_token` function
    is typically used to handle exceptions related to invalid credentials or unauthorized access. It is
    raised when there is an issue with the token verification process, such as an expired token or
    invalid token format
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

async def get_current_user(data: str = Depends(oauth2_scheme)):
    """
    Verifies the OAuth2 token provided in the `data` parameter.
    
    :param data: The `data` parameter in the `get_current_user` function is a string that represents the
    credentials obtained from the OAuth2 scheme. It is passed as a dependency using
    `Depends(oauth2_scheme)`
    :type data: str
    :return: The `get_current_user` function is returning the result of calling the `verify_token`
    function with the `data` parameter and the `credentials_exception` as an argument.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verify_token(data, credentials_exception)
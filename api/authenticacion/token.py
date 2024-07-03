from datetime import timedelta, datetime
from typing import Optional

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session

from api.database.personas import db_get_user_by_nombre
from api.database.settings import get_session
from api.error import UNAuthorizedException, QueryDBException
from api.settings import auth_setting

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Creacion de token para authenticacion
    Args:
        data: datos a encriptar en el token
        expires_delta: tiempo maxima de duracion del token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=auth_setting.tiempo_expiracion)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, auth_setting.secret_key, algorithm=auth_setting.algoritmo)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    """Validar el token de authorizacion y retornar el usuario

    Args:
        token: token de validacion
        session: session de la base de datos
    """
    try:
        payload = jwt.decode(token, auth_setting.secret_key, algorithms=[auth_setting.algoritmo])
        unique_number: str = payload.get("sub")
        if unique_number is None:
            raise UNAuthorizedException
    except jwt.InvalidTokenError:
        raise UNAuthorizedException
    try:
        user = db_get_user_by_nombre(unique_number, session)
    except QueryDBException:
        raise UNAuthorizedException
    return user

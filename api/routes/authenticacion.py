from datetime import timedelta
from fastapi import HTTPException, APIRouter, Depends, Query
from sqlmodel import Session
from starlette import status

from api.authenticacion.token import create_access_token
from api.database.oficiales import db_get_oficial_by_numero_unico
from api.database.settings import get_session
from api.database.tablas import Oficiales

router = APIRouter()


@router.get("/login", response_model=dict)
async def login_for_access_token(
        uid: str = Query(...),
        session: Session = Depends(get_session)
):
    oficial: Oficiales = db_get_oficial_by_numero_unico(uid, session)
    if not oficial:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Oficial not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": oficial.numero_unico}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

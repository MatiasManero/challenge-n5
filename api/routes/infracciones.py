from typing import List
from fastapi import APIRouter, Depends
from sqlmodel import Session
from api.authenticacion.token import get_current_user
from api.database.infraccion import db_get_informe, db_post_infraccion
from api.database.settings import get_session
from api.database.tablas import Infracciones
from api.routes.models import InfraccionBase

router = APIRouter()


@router.get(
    "/generar_informe",
    description="Cargar Infraccion.",
    response_model=List[InfraccionBase]
)
def get_generar_informe(
    email: str,
    session: Session = Depends(get_session)
) -> List[InfraccionBase]:
    """ Se genera un informe de las infracciones de una persona

    Args:
        email: email de la persona
        session: Session de base de datos
    """
    return db_get_informe(email, session)


@router.post(
    "/cargar_infraccion",
    description="Cargar Infraccion."
)
def post_cargar_infraccion(
    infraccion: InfraccionBase,
    session: Session = Depends(get_session),
    _: str = Depends(get_current_user)
):
    """ Endpoint para cargar infracciones
    Args:
        infraccion: Datos que se quieren cargar
        session: Session de Base de datos
        _: Authenticacion del usuario
    :return:
    """
    return db_post_infraccion(Infracciones(**infraccion.serialize()), session)


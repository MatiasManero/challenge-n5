from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select
from api.database.tablas import Vehiculos, Personas, Infracciones
from api.error import ResourceNotFoundException, QueryDBException
from api.logger import logger


def db_get_informe(email: str, session: Session):
    statement = (
        select(Infracciones)
        .join(Vehiculos)
        .join(Personas)
        .where(Personas.correo_electronico == email)
    )
    try:
        informe = session.exec(statement).all()
    except Exception as e:
        logger.exception(f"Ocurrio un error al intentar obtener el informe de {email}")
        raise QueryDBException()

    return informe


def db_post_infraccion(infraccion: Infracciones, session: Session):
    try:
        session.add(infraccion)
        session.commit()
    except IntegrityError:
        logger.exception("Ocurrio un error al cargar la infraccion")
        raise ResourceNotFoundException(detail=f"Patente {infraccion.placa_patente} no encontrada")
    except Exception as e:
        session.rollback()
        logger.exception(f"Ocurrio un error al cargar la infraccion {infraccion.dict()}")
        raise QueryDBException()

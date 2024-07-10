from sqlalchemy.exc import NoResultFound
from sqlmodel import select, Session

from api.database.tablas import Oficiales
from api.error import QueryDBException
from api.logger import logger


def db_get_oficial_by_numero_unico(uid: str, session: Session):
    """ Se consulta a la base de datos por un oficial filtrado por su numero unico
    Args:
        uid: Numero unico del oficial
        session: Session de base de datos
    """
    statement = select(Oficiales).where(Oficiales.numero_unico == uid)
    oficial = None
    try:
        oficial = session.exec(statement).one()
    except NoResultFound:
        pass
    except Exception as ex:
        err_msg = f"Error when consulting for the oficial with ui: {uid}"
        logger.exception(err_msg)
        raise QueryDBException(detail=err_msg)

    return oficial

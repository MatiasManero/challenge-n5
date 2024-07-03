from sqlalchemy.exc import NoResultFound
from sqlmodel import select, Session

from api.database.tablas import Oficiales
from api.error import QueryDBException
from api.logger import logger


def db_get_user_by_nombre(uid: str, session: Session):
    statement = select(Oficiales).where(Oficiales.numero_unico == uid)
    users = None
    try:
        users = session.exec(statement).one()
    except NoResultFound:
        pass
    except Exception as ex:
        err_msg = f"Error when consulting for the oficial with ui: {uid}"
        logger.exception(err_msg)
        raise QueryDBException(detail=err_msg)

    return users

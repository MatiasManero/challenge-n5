from fastapi import HTTPException


class BaseCustomException(HTTPException):
    def __init__(
            self,
            status_code: int = 500,
            detail: str = "Ocurrio un error al manejar la request"
    ):
        super().__init__(status_code=status_code, detail=detail)


class ResourceNotFoundException(BaseCustomException):
    def __init__(
            self,
            status_code: int = 404,
            detail: str = "No se encontro el recurso requerido"
    ):
        super().__init__(status_code=status_code, detail=detail)


class QueryDBException(BaseCustomException):
    def __init__(
            self,
            status_code: int = 500,
            detail: str = "Ocurrio un problema al intentar acceder a la base de datos"
    ):
        super().__init__(status_code=status_code, detail=detail)


class UNAuthorizedException(BaseCustomException):
    def __init__(
            self,
            status_code: int = 401,
            detail: str = "Could not validate credentials"
    ):
        super().__init__(status_code=status_code, detail=detail)

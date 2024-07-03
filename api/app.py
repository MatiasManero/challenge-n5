from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse
from api.database.settings import create_database_and_tables
from api.routes.infracciones import router as infracciones
from api.routes.authenticacion import router as login
from api.schema.schemas import site

app = FastAPI()
app.include_router(infracciones)
app.include_router(login)
# mount AdminSite instance
site.mount_app(app)


@app.on_event("startup")
def startup():
    create_database_and_tables()


@app.exception_handler(HTTPException)
async def validation_exception_handler(_: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


@app.exception_handler(Exception)
async def validation_exception_handler(_: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": f"Se produjo un error: {str(exc)}"},
    )

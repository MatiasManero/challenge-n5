import uvicorn
from api.app import app
from api.settings import api_settings

if __name__ == '__main__':
    uvicorn.run(
        app,
        host=api_settings.host,
        port=api_settings.port
    )
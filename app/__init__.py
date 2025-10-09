import logging

from fastapi import FastAPI
# delete next line, solo es usada en desarrollo
from fastapi.middleware.cors import CORSMiddleware ## alert -> delete this line or not commit it

logging.basicConfig(
    format="%(asctime)s - %(levelname)s : %(module)s - %(funcName)s | %(message)s",
    level=logging.INFO
)

app = FastAPI(
    title="Backend Controller API - Antillean",
    description=(
        "controller app"
    ),
    version="0.0.1",
    contact=
        {
            "name": "Nicolás Suárez"
        }
    ,
    license_info={
        "name": "©AXD",
        "url": "https://opensource.org/licenses/MIT",
    },
    openapi_url="/v1/api/openapi.json",
    docs_url="/v1/api/docs",
    redoc_url="/v1/api/redoc",
)

# delete this block, solo es usado en desarrollo  ## alert -> delete this block or not commit it
origins = [
    "http://localhost:4200",
    "http://localhost",
    "http://localhost:8080",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Permite los orígenes especificados
    allow_credentials=True, # Permite cookies/credenciales
    allow_methods=["*"],    # Permite todos los métodos (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],    # Permite todas las cabeceras (incluyendo Authorization)
)
# end delete block
from .views import *
import logging
import os
from dotenv import load_dotenv
load_dotenv()

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
    version="0.0.5",
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
origins = ["https://antillean.app/"]
# CORS opcional solo si ENABLE_DEV_CORS=true
if os.getenv("ENABLE_DEV_CORS", "false").lower() == "true":
    origins.append(os.getenv("DEV_UI_ORIGIN", "http://localhost:4200"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from .views import *
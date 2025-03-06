## Prueba de API de coxexion
from fastapi import APIRouter

entry_root = APIRouter()

#ENDPOINT
@entry_root.get("/api")
def apiRunning():
    res = {
        "status" : "ok",
        "message" : "Api esta corriendo",
    }
    return res


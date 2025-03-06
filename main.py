import os
from typing import Optional
from bson import ObjectId
from fastapi import FastAPI, Request, Form, File, UploadFile
from routes.entry import entry_root
from routes.historias import historias_root
from starlette.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
from config.config import historias_collection, obtener_historia_por_id, upload_folder
from models.historias import HistoriasModel

templates = Jinja2Templates(directory="templates")

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.include_router(entry_root)
app.include_router(historias_root)

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/inicio")
async def inicio(request: Request):
    return templates.TemplateResponse("inicio.html", {"request": request})

@app.get("/search")
async def search(request: Request):
    return templates.TemplateResponse("search.html", {"request": request})

# Ruta para ver historias
@app.get("/VerHistorias")
async def ver_historias(request: Request):
    return templates.TemplateResponse("VerHistorias.html", {"request": request})

# Ruta para ver una historia
@app.get("/VerHistoria/{id}")
async def ver_historia(request: Request, id: str):
    historia = historias_collection.find_one({"_id": ObjectId(id)})
    if historia is None:
        return {"status": "Error", "message": "No se encontró la historia"}
    return templates.TemplateResponse("VerHistoria.html", {
        "request": request,
        "historia": historia
    })

# Ruta Leer Historia
@app.get("/LeerHistoria/{id}")
async def leer_historia(request: Request, id: str):
    historia = historias_collection.find_one({"_id": ObjectId(id)})
    if historia is None:
        return {"status": "Error", "message": "No se encontró la historia"}
    return templates.TemplateResponse("LeerHistoria.html", {
        "request": request,
        "historia": historia
    })

# Ruta para crear una nueva historia
@app.get("/NewHistoria")
async def new_historia(request: Request):
    return templates.TemplateResponse("NewHistoria.html", {"request": request})

# Ruta De Info de Historia
@app.get("/InfoHistoria/{id}")
async def info_historia(request: Request, id: str):
    historia = historias_collection.find_one({"_id": ObjectId(id)})
    if historia is None:
        return {"status": "Error", "message": "No se encontró la historia"}
    return templates.TemplateResponse("InfoHistoria.html", {
        "request": request,
        "historia": historia
    })

# Ruta Ver Historias y Editar
@app.get("/ListHistorias")
async def list_historias(request: Request):
    return templates.TemplateResponse("ListHistorias.html", {"request": request})


# Ruta Editar Historia
@app.get("/EditarHistoria/{id}")
async def editar_historia(request: Request, id: str):
    historia = await obtener_historia_por_id(id)
    if historia is None:
        return {"status": "Error", "message": "No se encontró la historia"}
    historia = dict(historia)
    return templates.TemplateResponse("EditarHistoria.html", {"request": request, "historia": historia})

# Buscador
# Ruta para mostrar el template Categorias.html
@app.get("/Categorias")
async def mostrar_categorias(request: Request):
    categorias = historias_collection.distinct("categoria")
    return templates.TemplateResponse("Categorias.html", {"request": request, "categorias": categorias})

# Ruta para buscar historias por categoría
@app.get("/Categorias/{categoria}")
async def buscar_historias(request: Request, categoria: str):
    historias = historias_collection.find({"categoria": categoria})
    historias_list = []
    for historia in historias:
        historia["_id"] = str(historia["_id"])
        historias_list.append(historia)
    return templates.TemplateResponse("Categorias.html", {"request": request, "historias": historias_list, "categoria": categoria})
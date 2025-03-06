from typing import List
from fastapi import APIRouter, Form, Request
from models.historias import HistoriasModel, UpdateHistoriasModel
from config.config import historias_collection, upload_folder
from serializers.historias import DecodeHistorias, DecodeHistoria
from bson import ObjectId
import os
from fastapi import File, UploadFile
from fastapi.responses import JSONResponse, RedirectResponse
from datetime import datetime

historias_root = APIRouter()

# CREADOR DE NUEVA HISTORIA
@historias_root.post("/NewHistoria")
async def create_historia(
    nombre_historia: str = Form(...),
    fecha_de_la_leyenda: int = Form(...),
    descripcion_de_historia: str = Form(...),
    categoria: List[str] = Form(...),  # Recibe la lista de categorías como un array
    distrito: str = Form(...),
    historia: str = Form(...),
    imagen: UploadFile = File(...),
):
    # Crea un nuevo documento en la base de datos
    fecha_subida = datetime.now().strftime("%d/%m/%Y")
    doc = {
        "nombre_historia": nombre_historia,
        "fecha_de_la_leyenda": fecha_de_la_leyenda,
        "descripcion_de_historia": descripcion_de_historia,
        "categoria": categoria,  # Guarda la lista de categorías en la base de datos
        "distrito": distrito,
        "historia": historia,
        "fecha_subida": fecha_subida
    }

    # Guarda el documento en la base de datos
    res = historias_collection.insert_one(doc)
    doc_id = str(res.inserted_id)

    # Llama a la función upload_image para guardar la imagen
    await upload_image(doc_id, imagen)

    # Actualiza el documento para asegurarte de que la fecha de subida se guarde correctamente
    historias_collection.update_one({"_id": ObjectId(doc_id)}, {"$set": {"fecha_subida": fecha_subida}})

    return RedirectResponse(url=f"/InfoHistoria/{doc_id}", status_code=302)

# LISTAR O BUSCAR TODAS LAS HISTORIAS
@historias_root.get("/all/historias")
def AllHistorias():
    res = historias_collection.find()
    decode_data = DecodeHistorias(res)

    return {
        "status": "Ok",
        "data": decode_data,
    }

# LISTAR UNA HISTORIA ESPECIFICA
@historias_root.get("/historia/{_id}")
def GetHistoria(_id: str):
    res = historias_collection.find_one({"_id": ObjectId(_id)})
    decoded_historias = DecodeHistoria(res)

    return {
        "status": "Ok",
        "data": decoded_historias,
    }


# ACTUALIZAR LAS HISTORIAS
@historias_root.post("/update")
async def UpdateHistorias(
    method: str = Form(...), 
    id: str = Form(...), 
    nombre_historia: str = Form(...), 
    descripcion_de_historia: str = Form(...), 
    fecha_de_la_leyenda: int = Form(...), 
    categoria: List[str] = Form(...), 
    distrito: str = Form(...), 
    historia: str = Form(...), 
    imagen: UploadFile = File(None)
):
    if method == "patch":
        # Actualiza la historia
        update_data = {
            "nombre_historia": nombre_historia,
            "descripcion_de_historia": descripcion_de_historia,
            "fecha_de_la_leyenda": fecha_de_la_leyenda,
            "categoria": categoria,
            "distrito": distrito,
            "historia": historia
        }

        # Verifica si se ha subido una nueva imagen
        if imagen:
            # Guarda la nueva imagen en el servidor
            filename = imagen.filename
            file_path = os.path.join(upload_folder, filename)
            with open(file_path, "wb") as f:
                f.write(imagen.file.read())

            # Actualiza la ruta de la imagen en la base de datos
            update_data["imagen"] = f"uploads/{filename}"

        historias_collection.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": update_data}
        )

        return RedirectResponse(url=f"/InfoHistoria/{id}", status_code=302)
    else:
        return {"error": "Método no permitido"}

# ELIMINAR HISTORIA
@historias_root.delete("/InfoHistoria/{_id}")
def DeleteHistorias(_id: str):
    historias_collection.find_one_and_delete(
        {"_id": ObjectId(_id)}
    )
    return {
        "status": "Ok",
        "message": "Historia Eliminada Correctamente"
    }

# ACTUALIZAR IMAGENES A LA CARPETA PARA DESPUES VISUALIZARLA
@historias_root.post("/upload-image/{_id}")
async def upload_image(_id: str, image: UploadFile = File(...)):
    try:
        # Verifica si el archivo subido es una imagen
        if image.content_type not in ["image/jpeg", "image/png", "image/gif"]:
            return JSONResponse(content={"message": "Solo se permiten archivos de imagen (JPEG, PNG, GIF)"}, media_type="application/json", status_code=400)
        
        # Guarda la imagen en el servidor
        with open(os.path.join(upload_folder, image.filename), "wb") as f:
            f.write(image.file.read())
        
        # Actualiza la historia con la ruta de la imagen
        historias_collection.find_one_and_update(
            {"_id": ObjectId(_id)},
            {"$set": {"imagen": f"uploads/{image.filename}"}}
        )
        
        # Retorna la ruta de la imagen
        return JSONResponse(content={"message": "Imagen subida correctamente", "image_url": f"{upload_folder}/{image.filename}"}, media_type="application/json")
    
    except Exception as e:
        return JSONResponse(content={"message": "Error al subir la imagen", "error": str(e)}, media_type="application/json", status_code=500)


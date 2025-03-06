## Models para la base de datos
from pydantic import BaseModel
from typing import List

class HistoriasModel(BaseModel):
    imagen: str = None
    nombre_historia: str
    fecha_de_la_leyenda: int
    fecha_de_subida: str = None
    descripcion_de_historia: str
    categoria: List[str]
    distrito: str
    historia: str


class UpdateHistoriasModel(BaseModel):
    imagen: str = None
    nombre_historia: str = None
    fecha_de_la_leyenda: int = None
    fecha_de_subida: str = None
    descripcion_de_historia: str = None
    categoria: List[str] = None
    distrito: str = None
    historia: str = None
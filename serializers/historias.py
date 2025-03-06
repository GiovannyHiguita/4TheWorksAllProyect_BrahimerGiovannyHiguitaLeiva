## FUNCION PARA CONVERTIR DATOS
def DecodeHistoria(doc) -> dict:
    return {
        "_id": str(doc["_id"]),
        "imagen": doc["imagen"],
        "nombre_historia": doc["nombre_historia"],
        "fecha_de_la_leyenda": doc["fecha_de_la_leyenda"],
        "descripcion_de_historia": doc["descripcion_de_historia"],
        "categoria": doc["categoria"],
        "distrito": doc["distrito"],
        "historia": doc["historia"],
    }

# LISTA DE DOCUMENTOS
def DecodeHistorias(docs) -> list:
    return [DecodeHistoria(doc) for doc in docs]
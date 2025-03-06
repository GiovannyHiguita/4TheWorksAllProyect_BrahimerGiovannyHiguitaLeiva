from bson import ObjectId
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://python:987654321@cluster0.mungn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
db = client.LeyendasCR
historias_collection = db["Leyendas"]

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

# Devulve info a la base de datos
async def obtener_historia_por_id(id: str):
    historia = historias_collection.find_one({"_id": ObjectId(id)})
    return historia

# Ruta para subir imágenes
upload_folder = "uploads"
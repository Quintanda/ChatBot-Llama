from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId

# Conexão com o MongoDB Atlas
MONGO_URI = "mongodb+srv://marcelo:marcelo1234@mycluster.4kvwvjs.mongodb.net/?retryWrites=true&w=majority&appName=myCluster"  # Substitua com sua URI do MongoDB Atlas
client = MongoClient(MONGO_URI)
db = client["chat_database"]  # Nome do banco de dados
messages_collection = db["messages"]  # Nome da coleção

# Inicialização da API
app = FastAPI()

# Modelo para a entrada de mensagens
class Message(BaseModel):
    chat_id: str
    user: str
    message: str

@app.post("/messages")
def store_message(message: Message):
    """
    Armazena uma mensagem no MongoDB para um chat específico.
    """
    message_data = {
        "chat_id": message.chat_id,
        "user": message.user,
        "message": message.message,
        "timestamp": datetime.utcnow()
    }
    result = messages_collection.insert_one(message_data)
    if result.inserted_id:
        return {"message": "Mensagem armazenada com sucesso!", "id": str(result.inserted_id)}
    else:
        raise HTTPException(status_code=500, detail="Erro ao armazenar a mensagem")

@app.get("/messages/{chat_id}")
def get_messages(chat_id: str):
    """
    Retorna o histórico de mensagens de um chat específico.
    """
    messages = []
    for msg in messages_collection.find({"chat_id": chat_id}).sort("timestamp", 1):
        messages.append({
            "id": str(msg["_id"]),
            "user": msg["user"],
            "message": msg["message"],
            "timestamp": msg["timestamp"]
        })
    return {"chat_id": chat_id, "messages": messages}

# Endpoint para teste de conexão
@app.get("/")
def home():
    return {"message": "API de histórico de mensagens está funcionando!"}

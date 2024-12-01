from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModel
import torch

# Inicialize o modelo e o tokenizer
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"  # Modelo de embeddings popular
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModel.from_pretrained(MODEL_NAME)

# Inicialize o FastAPI
app = FastAPI()

# Estrutura para entrada de texto
class TextInput(BaseModel):
    text: str

@app.post("/embedding")
def generate_embedding(input: TextInput):
    """
    Gera embedding para o texto fornecido.
    """
    # Tokenize o texto
    inputs = tokenizer(input.text, return_tensors="pt", padding=True, truncation=True)
    
    # Geração dos embeddings
    with torch.no_grad():
        outputs = model(**inputs)
        # Use a saída do modelo (camada [0] geralmente é o embedding de última camada)
        embeddings = outputs.last_hidden_state.mean(dim=1).squeeze().tolist()

    return {"embedding": embeddings}

@app.get("/")
def home():
    return {"message": "API de Embeddings está funcionando!"}

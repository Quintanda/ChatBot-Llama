from fastapi import FastAPI
from pydantic import BaseModel
import requests
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

app = FastAPI()

# URL do serviço de embeddings
EMBEDDINGS_SERVICE_URL = "http://localhost:8000/embedding"

# Estrutura das intenções e exemplos
intents = {
    "greeting": ["Olá", "Oi", "Tudo bem?", "Bom dia", "Boa tarde", "Boa noite", "E aí?", "Oi, tudo bom?", "Oi, como você está?", "Saudações"],
    "farewell": ["Tchau", "Até logo", "Até mais", "Falamos depois", "Obrigado, até a próxima", "Tenha um bom dia", "Nos vemos em breve", "Até a próxima", "Tchau, boa noite", "Vou nessa"],
    "help": ["Preciso de ajuda", "Pode me ajudar?", "Como funciona?", "O que posso fazer aqui?", "Pode explicar?", "Estou com dúvidas", "Me ajuda, por favor", "Quero saber como fazer", "Não sei o que fazer", "Preciso de informações"],
    "gratitude": ["Obrigado", "Muito obrigado", "Valeu", "Agradeço pela ajuda", "Você foi muito útil", "Obrigadão", "Agradeço muito", "Fico muito grato", "Gratidão", "Valeu mesmo"],
}


# Requisita o embedding de todos os intents e salva em 'intent_embeddings'
def get_intent_embeddings():
    embeddings = {}
    for intent, examples in intents.items():
        # Combina todas as frases representativas em um texto
        combined_text = " ".join(examples)
        response = requests.post(EMBEDDINGS_SERVICE_URL, json={"text": combined_text})
        response.raise_for_status()  # Garantir que não há erro
        embeddings[intent] = np.array(response.json()["embedding"])
    return embeddings

intent_embeddings = get_intent_embeddings() # Salva os embeddings

# Modelo de entrada do usuário
class UserInput(BaseModel):
    text: str

@app.post("/intent")
def get_intent(input: UserInput):
    
    # Recebe o texto do usuário e retorna a intenção mais próxima.
    
    # Obter o embedding do texto do usuário
    response = requests.post(EMBEDDINGS_SERVICE_URL, json={"text": input.text})
    response.raise_for_status()
    user_embedding = np.array(response.json()["embedding"])

    # Comparar com os embeddings das intenções
    best_intent = None
    best_score = -1

    for intent, embedding in intent_embeddings.items():
        score = cosine_similarity([user_embedding], [embedding]).flatten()[0]
        if score > best_score:
            best_score = score
            best_intent = intent

    return {"intent": best_intent, "confidence": best_score}

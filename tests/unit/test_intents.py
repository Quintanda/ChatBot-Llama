import requests

# URL da API de Intents
API_URL = "https://quintanda-intent-detection.hf.space/intent"

# Frases de teste com suas intenções esperadas
test_cases = [
    # Saudações (greeting)
    {"text": "Oi", "expected_intent": "greeting"},
    {"text": "Olá, tudo bem?", "expected_intent": "greeting"},
    {"text": "Boa tarde, como você está?", "expected_intent": "greeting"},
    {"text": "E aí, tudo certo?", "expected_intent": "greeting"},
    {"text": "Oi, bom dia", "expected_intent": "greeting"},
    {"text": "Boa noite, tudo tranquilo?", "expected_intent": "greeting"},

    # Despedidas (farewell)
    {"text": "Tchau, até a próxima", "expected_intent": "farewell"},
    {"text": "Até mais", "expected_intent": "farewell"},
    {"text": "Valeu, até logo", "expected_intent": "farewell"},
    {"text": "Obrigado, tchau", "expected_intent": "farewell"},
    {"text": "Falamos depois", "expected_intent": "farewell"},
    {"text": "Vou nessa, até mais", "expected_intent": "farewell"},

    # Gratidão (gratitude)
    {"text": "Muito obrigado pela ajuda", "expected_intent": "gratitude"},
    {"text": "Agradeço muito", "expected_intent": "gratitude"},
    {"text": "Você foi muito útil, obrigado", "expected_intent": "gratitude"},
    {"text": "Valeu mesmo", "expected_intent": "gratitude"},
    {"text": "Obrigado por tudo", "expected_intent": "gratitude"},
    {"text": "Gratidão", "expected_intent": "gratitude"},

    # Pedido de ajuda (help)
    {"text": "Preciso de ajuda com meu pedido", "expected_intent": "help"},
    {"text": "Você pode me ajudar?", "expected_intent": "help"},
    {"text": "Estou com uma dúvida", "expected_intent": "help"},
    {"text": "Me explica como funciona?", "expected_intent": "help"},
    {"text": "Não sei como resolver isso", "expected_intent": "help"},
    {"text": "Como faço para resolver isso?", "expected_intent": "help"},
]

# Função para testar cada caso
def test_intents():
    for case in test_cases:
        # Enviar a requisição para a API
        response = requests.post(API_URL, json={"text": case["text"]})
        
        # Verificar se a requisição foi bem-sucedida
        if response.status_code == 200:
            # Obter a resposta JSON
            data = response.json()
            predicted_intent = data.get("intent", None)
            
            # Exibir o resultado do teste
            print(f"Frase: '{case['text']}'")
            print(f"Intenção esperada: {case['expected_intent']}")
            print(f"Intenção prevista: {predicted_intent}")
            
            # Verificar se corresponde ao esperado
            if predicted_intent == case["expected_intent"]:
                print("Resultado: ✅ Correto")
            else:
                print("Resultado: ❌ Incorreto")
        else:
            print(f"Erro na API para a frase '{case['text']}'. Status Code: {response.status_code}")
        
        print("-" * 50)

# Executar os testes
if __name__ == "__main__":
    test_intents()

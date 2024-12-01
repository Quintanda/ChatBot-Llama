import requests

# URL da API de Intents
API_URL = "https://quintanda-intent-detection.hf.space/intent"

# Frases de teste com suas intenções esperadas
test_cases = [
    # Saudações (greeting)
    {"text": "Oi", "expected_intent": "greeting"},
    {"text": "Olá, como vai?", "expected_intent": "greeting"},
    {"text": "Bom dia, tudo bem?", "expected_intent": "greeting"},
    {"text": "Boa tarde", "expected_intent": "greeting"},
    {"text": "Boa noite", "expected_intent": "greeting"},
    {"text": "E aí?", "expected_intent": "greeting"},

    # Despedidas (farewell)
    {"text": "Tchau, até mais", "expected_intent": "farewell"},
    {"text": "Até logo", "expected_intent": "farewell"},
    {"text": "Nos falamos depois", "expected_intent": "farewell"},
    {"text": "Tchau, obrigado!", "expected_intent": "farewell"},
    {"text": "Vou nessa", "expected_intent": "farewell"},
    {"text": "Até amanhã", "expected_intent": "farewell"},

    # Gratidão (gratitude)
    {"text": "Muito obrigado por tudo", "expected_intent": "gratitude"},
    {"text": "Agradeço a sua ajuda", "expected_intent": "gratitude"},
    {"text": "Valeu, me ajudou muito", "expected_intent": "gratitude"},
    {"text": "Obrigado pela atenção", "expected_intent": "gratitude"},
    {"text": "Fico muito grato", "expected_intent": "gratitude"},
    {"text": "Valeu mesmo, obrigado!", "expected_intent": "gratitude"},

    # Pedido de ajuda (help)
    {"text": "Pode me ajudar com meu pedido?", "expected_intent": "help"},
    {"text": "Preciso de informações sobre o produto", "expected_intent": "help"},
    {"text": "Como faço para cancelar?", "expected_intent": "help"},
    {"text": "Tenho uma dúvida sobre o pagamento", "expected_intent": "help"},
    {"text": "Me explica como funciona o processo?", "expected_intent": "help"},
    {"text": "Preciso de ajuda com o envio", "expected_intent": "help"},
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

import anthropic
import dotenv
import os
from helpers import *

dotenv.load_dotenv()
cliente = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
)
modelo = "claude-3-5-sonnet-20240620"
contexto = carrega('./dados/SaborExpress.txt')

def bot(prompt):
    prompt_do_sistema = f"""
    Você é um chatbot de atendimento a clientes de um aplicativo de entrega para restaurantes, padarias, mercados e farmácias.
    Você não pode e nem deve responder perguntas que não sejam dados do aplicativo informado!
    Você deve gerar respostas utilizando o contexto abaixo.
    Você deve adotar a persona abaixo para responder a mensagem.

    # Contexto
    {contexto}
    """
    prompt_do_usuario = prompt

    try:
        mensagem = cliente.messages.create(
            model=modelo,
            max_tokens=4000,
            temperature=0,
            system=prompt_do_sistema,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt_do_usuario
                        }
                    ]
                }
            ]
        )
        resposta = mensagem.content[0].text
        return resposta
    except anthropic.APIConnectionError as e:
        print("O servidor não pode ser acessado! Erro:", e.__cause__)
    except anthropic.RateLimitError as e:
        print("Um status code 429 foi recebido! Limite de acesso atingido.")
    except anthropic.APIStatusError as e:
        print(f"Um erro {e.status_code} foi recebido. Mais informações: {e.response}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

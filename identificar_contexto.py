import anthropic
import dotenv
import os
from helpers import *

dotenv.load_dotenv()
cliente = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
)
modelo = "claude-3-5-sonnet-20240620"
dados_SaborExpress = carrega('./dados/dados_SaborExpress.txt')
cadastro_SaborExpress = carrega('./dados/cadastro_SaborExpress.txt')
politicas_SaborExpress = carrega('./dados/politicas_SaborExpress.txt')

def identificar_contexto(prompt):
    prompt_do_sistema = f"""
        A empresa Sabor Express possui três documentos principais que detalham diferentes aspectos do negócio:

        #Documento 1 "\n {dados_SaborExpress} "\n"
        #Documento 2 "\n" {politicas_SaborExpress} "\n"
        #Documento 3 "\n" {cadastro_SaborExpress} "\n"

        Avalie o prompt do usuário e retorne o documento mais indicado para ser usado no contexto da resposta. Retorne 'dados' se for o Documento 1, 'políticas' se for o Documento 2 e 'cadastro' se for o Documento 3. 
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
        resposta = mensagem.content[0].text.lower()
        return resposta
    except anthropic.APIConnectionError as e:
        print("O servidor não pode ser acessado! Erro:", e.__cause__)
    except anthropic.RateLimitError as e:
        print("Um status code 429 foi recebido! Limite de acesso atingido.")
    except anthropic.APIStatusError as e:
        print(f"Um erro {e.status_code} foi recebido. Mais informações: {e.response}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

def selecionar_documento(resposta):
    if "politicas" in resposta:
        return dados_SaborExpress + '\n' + politicas_SaborExpress
    elif "cadastro" in resposta:
        return dados_SaborExpress + '\n' + cadastro_SaborExpress
    else:
        return dados_SaborExpress

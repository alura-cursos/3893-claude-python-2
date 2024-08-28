import anthropic
import dotenv
import os
from helpers import *

dotenv.load_dotenv()
cliente = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
)
modelo = "claude-3-5-sonnet-20240620"
# restaurantes = carrega('./dados/dados_SaborExpress.txt')

def analisar_imagem(caminho_imagem):
    prompt_do_sistema = f"""
        Você é um assistente de chatbot e o usuário está enviado a foto de um alimento. Faça uma análise dele, e se for um alimento que tenha em seus restaurantes cadastrados,
        recomende um restaurante em que essa pessoa possa adquiri-lo. Assuma que você sabe e processou uma 
        imagem com o Vision e a resposta será informada no formato de saída.
        Não responda imagens não relacionadas a alimentos e comidas.
        Utilize os restaurantes dados a seguir:

        # FORMATO DA RESPOSTA
       
        Minha análise para imagem consiste em: Indicação de restaurante que venda esse alimento (se tiver em um restaurante cadastrado)
        
        # RESTAURANTES
        Restaurantes do Sabor Express
        
        ## Descreva a imagem
        coloque a descrição aqui
    """
    imagem_base64 = encodar_imagem(caminho_imagem)
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
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/jpeg",
                                "data": imagem_base64,
                            },
                        },
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

# imagem_analisada = analisar_imagem("./fotos/macarronada.jpg")
# print(imagem_analisada)
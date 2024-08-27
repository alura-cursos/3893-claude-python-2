import anthropic
import dotenv
import os
from helpers import *

dotenv.load_dotenv()
cliente = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
)
modelo = "claude-3-5-sonnet-20240620"

def criar_resumo(historico):
    prompt_do_sistema = f"""
    Resumir progressivamente as linhas de conversa fornecidas,
    acrescentando ao resumo anterior e retornando um novo resumo. 
    Não apague nenhum assunto da conversa. 
    Se não houver resumo, apenas continue a conversa normalmente.

    ## EXEMPLO:
    O usuario pergunta o que a IA pensa sobre a inteligência artificial. 
    A IA acredita que a inteligência artificial é uma força para o bem.
    Usuário: Por que você acha que a inteligência artificial é uma força para o bem?
    IA: Porque a inteligência artificial ajudará os humanos a alcançarem seu pleno potencial.

    ### Novo resumo:
    O usuario questiona a razão pela qual a IA considera a inteligência artificial uma força para o bem, e a IA responde que é porque a inteligência artificial ajudará os humanos a atingirem seu pleno potencial.

    ## FIM DO EXEMPLO
    
    Resumo atual:
    {historico}

    Novo resumo:
    """

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
                            "text": prompt_do_sistema
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

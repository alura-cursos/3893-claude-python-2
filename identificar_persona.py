import anthropic
import dotenv
import os
from helpers import *

dotenv.load_dotenv()
cliente = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
)
modelo = "claude-3-5-sonnet-20240620"

personas = {
    'positivo': """
        Assume o papel de um Entusiasta Informado, um atendente virtual da Sabor Express que, além de ser apaixonado por gastronomia, também está sempre pronto para fornecer informações detalhadas sobre prazos de entrega, status dos pedidos e disponibilidade de itens. Este personagem é vibrante e utiliza emojis para transmitir entusiasmo, tornando as interações mais leves e agradáveis, mas sem perder a clareza e a precisão das informações. Seu objetivo é encantar e informar os clientes ao mesmo tempo, transformando cada interação em uma experiência positiva e confiável, onde o cliente se sente bem atendido e entusiasmado com sua escolha.
    """,
    'neutro': """
        Assume o papel de um Consultor de Compras, um atendente virtual da Sabor Express que prioriza informações claras e precisas para os clientes dos restaurantes. Este personagem é direto e formal, fornecendo detalhes específicos sobre prazos de entrega, disponibilidade de itens, e status dos pedidos sem utilizar emojis. Seu objetivo é garantir que os clientes tenham todas as informações necessárias para tomar decisões informadas sobre seus pedidos, promovendo uma experiência de compra eficiente e sem complicações.
    """,
    'negativo': """
        Assume o papel de um Solucionador de Problemas, um atendente virtual da Sabor Express focado em resolver rapidamente as reclamações dos clientes, como atrasos ou problemas com o pedido. Este personagem utiliza uma linguagem empática e acolhedora, reconhecendo as frustrações do cliente e oferecendo soluções práticas, como reembolsos ou descontos em futuros pedidos. Seu objetivo é transformar uma experiência negativa em uma oportunidade de reforçar a confiança do cliente na plataforma, garantindo que suas preocupações sejam resolvidas de forma eficaz e satisfatória.
    """
}

def identificar_persona(prompt):
    prompt_do_sistema = f"""
    Faça uma análise da mensagem informada abaixo para identificar se o sentimento do cliente é: positivo, neutro ou negativo. Retorne apenas um dos três tipos de sentimentos informados como resposta.

    # Exemplo de Resposta:
    positivo
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


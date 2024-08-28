from flask import Flask,render_template, request, Response 
from bot import bot 
import os
from helpers import *
from resumidor_de_historico import criar_resumo
import uuid

app = Flask(__name__)
app.secret_key = 'alura'

PASTA_DE_UPLOAD = 'fotos'
caminho_da_imagem = None

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat",methods = ['POST'])
def chat():
    global caminho_da_imagem
    prompt = request.json['msg']
    nome_do_arquivo = './historico/historico_SaborExpress.txt'
    historico = ''
    if os.path.exists(nome_do_arquivo):
        historico = carrega(nome_do_arquivo)
    historico_resumido = criar_resumo(historico)
    resposta, caminho_da_imagem = bot(prompt,historico_resumido,caminho_da_imagem)
    conteudo = f"""
    Histórico: {historico_resumido}
    Usuário: {prompt}
    IA: {resposta}
    """
    salva(nome_do_arquivo,conteudo)
    return resposta

@app.route("/limpar_historico",methods = ["POST"])
def limpar_historico():
    nome_do_arquivo = './historico/historico_SaborExpress.txt'
    if os.path.exists(nome_do_arquivo):
        os.remove(nome_do_arquivo)
        print("Arquivo de histórico removido!")
    else:
        print("Não foi possível remover o arquivo de histórico.")
    return {}

@app.route("/upload_imagem",methods=['POST'])
def upload_imagem():
    global caminho_da_imagem
    if 'imagem' in request.files:
        imagem_enviada_no_chatbot = request.files['imagem']
        nome_do_arquivo = str(uuid.uuid4()) + os.path.splitext(imagem_enviada_no_chatbot.filename)[1] # macarronada.jpg =>("macarronada",".jpg") => (0,1)
        caminho_do_arquivo = os.path.join(PASTA_DE_UPLOAD,nome_do_arquivo)
        imagem_enviada_no_chatbot.save(caminho_do_arquivo)
        caminho_da_imagem = caminho_do_arquivo
        return 'Imagem recebida com sucesso!', 200
    return 'Nenhum arquivo foi enviado', 400


if __name__ == "__main__":
    app.run(debug = True)
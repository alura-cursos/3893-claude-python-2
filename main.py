from flask import Flask,render_template, request, Response 
from bot import bot 
import os
from helpers import *
from resumidor_de_historico import criar_resumo

app = Flask(__name__)
app.secret_key = 'alura'

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat",methods = ['POST'])
def chat():
    prompt = request.json['msg']
    nome_do_arquivo = './historico/historico_SaborExpress.txt'
    historico = ''
    if os.path.exists(nome_do_arquivo):
        historico = carrega(nome_do_arquivo)
    historico_resumido = criar_resumo(historico)
    resposta = bot(prompt,historico_resumido)
    conteudo = f"""
    Histórico: {historico_resumido}
    Usuário: {prompt}
    IA: {resposta}
    """
    salva(nome_do_arquivo,conteudo)
    return resposta

if __name__ == "__main__":
    app.run(debug = True)
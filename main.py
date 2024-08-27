from flask import Flask,render_template, request, Response 
from bot import bot 
import os
from helpers import *

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
    resposta = bot(prompt,historico)
    conteudo = f"""
    Histórico: {historico}
    Usuário: {prompt}
    IA: {resposta}
    """
    salva(nome_do_arquivo,conteudo)
    return resposta

if __name__ == "__main__":
    app.run(debug = True)
from flask import Flask, jsonify, request
import json
import urllib.request
import random

app = Flask(__name__)

@app.route("/login/<string:usuario>/<string:senha>", methods=['GET'])
def login(usuario, senha):
    if usuario == "aluno" and senha == "impacta":
        return "SUCESSO"
    else:
        return "ERRO"


if __name__ == "__main__":
    app.run(host='0.0.0.0')
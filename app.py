from flask import Flask, jsonify, request
import json
import urllib.request
import random

app = Flask(__name__)

servicos = [{"id": e, "descricao": "Servico: "+str(e), "vl_obra": "500,00", "vl_total": "750,00", "dt_inicial": "01/11/2021", "dt_final": "15/11/2021", "imagem": "https://arcondicionadorefrival.com/wp-content/uploads/2019/02/como-instalar-ar-condicionado-split-1-e1549932371685.jpg"} for e in range(1, 16)]

usuario = [{"login": "aluno", "senha": "impacta"}]

@app.route("/usuario", methods=['GET'])
def get():
    return jsonify(usuario)

@app.route("/servicos", methods=['GET'])
def get_usuario():
    return jsonify(servicos)


@app.route("/servicos/<int:id>", methods=['GET'])
def get_one(id):
    filtro = [e for e in servicos if e["id"] == id]
    if filtro:
        return jsonify(filtro[0])
    else:
        return jsonify({})

@app.route("/servicos", methods=['POST'])
def post():
    global servicos
    try:
        content = request.get_json()

        # gerar id
        ids = [e["id"] for e in servicos]
        if ids:
            nid = max(ids) + 1
        else:
            nid = 1
        content["id"] = nid
        servicos.append(content)
        return jsonify({"status":"OK", "msg":"Servico adicionado com sucesso"})
    except Exception as ex:
        return jsonify({"status":"ERRO", "msg":str(ex)})


@app.route("/servicos/<int:id>", methods=['DELETE'])
def delete(id):
    global servicos
    try:
        servicos = [e for e in servicos if e["id"] != id]
        return jsonify({"status":"OK", "msg":"servico removido com sucesso"})
    except Exception as ex:
        return jsonify({"status":"ERRO", "msg":str(ex)})

@app.route("/push/<string:key>/<string:token>", methods=['GET'])
def push(key, token):
	s = random.choice(servicos)
	data = {
		"to": token,
		"notification" : {
			"title":s["descricao"],
			"body":"Um novo valor de obra foi adicionado em "+s['descricao']
		},
		"data" : {
			"servicoId":s['id']
		}
	}
	req = urllib.request.Request('http://fcm.googleapis.com/fcm/send')
	req.add_header('Content-Type', 'application/json')
	req.add_header('Authorization', 'key='+key)
	jsondata = json.dumps(data)
	jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes
	req.add_header('Content-Length', len(jsondataasbytes))
	response = urllib.request.urlopen(req, jsondataasbytes)
	print(response)
	return jsonify({"status":"OK", "msg":"Push enviado"})


@app.route("/login/<string:usuario>/<string:senha>", methods=['GET'])
def login(usuario, senha):
    if usuario == "aluno" and senha == "impacta":
        return "SUCESSO"
    else:
        return "ERRO"


if __name__ == "__main__":
    app.run(host='0.0.0.0')
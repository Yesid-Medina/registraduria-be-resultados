from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS
import json
from waitress import serve
import pymongo
import certifi

app = Flask(__name__)
cors = CORS(app)

from Controladores.ControladorCandidato import ControladorCandidato
miControladorCandidato=ControladorCandidato()

from Controladores.ControladorPartido import ControladorPartido
miControladorPartido=ControladorPartido()

from Controladores.ControladorMesa import ControladorMesa
miControladorMesa=ControladorMesa()

from Controladores.ControladorResultado import ControladorResultado
miControladorResultado=ControladorResultado()

#Conexion a mongodb

ca = certifi.where()
client = pymongo.MongoClient("mongodb+srv://Tatiana:Mnbv9874@proyecto.vaxnwo8.mongodb.net/proyecto-db?retryWrites=true&w=majority",tlsCAFile=ca)
db = client.test
print(db)

baseDatos = client["proyecto-db"]
print(baseDatos.list_collection_names())

# CRUD de candidato

@app.route("/",methods=['GET'])
def test():
    json = {}
    json["message"]="Server running ..."
    return jsonify(json)

@app.route("/candidato",methods=['GET'])
def getCandidatos():
    json=miControladorCandidato.index()
    return jsonify(json)

@app.route("/candidato",methods=['POST'])
def crearCandidato():
    data = request.get_json()
    json=miControladorCandidato.create(data)
    return jsonify(json)

@app.route("/candidato/<string:cedula>",methods=['GET'])
def getCandidato(cedula):
    json=miControladorCandidato.show(cedula)
    return jsonify(json)

@app.route("/candidato/<string:cedula>",methods=['PUT'])
def modificarCandidato(cedula):
    data = request.get_json()
    json=miControladorCandidato.update(cedula,data)
    return jsonify(json)

@app.route("/candidato/<string:cedula>",methods=['DELETE'])
def eliminarCandidato(cedula):
    json=miControladorCandidato.delete(cedula)
    return jsonify(json)

#CRUD de partido

@app.route("/partido",methods=['GET'])
def getPartidos():
    json=miControladorPartido.index()
    return jsonify(json)

@app.route("/partido",methods=['POST'])
def crearPartido():
    data = request.get_json()
    json=miControladorPartido.create(data)
    return jsonify(json)

@app.route("/partido/<string:id>",methods=['GET'])
def getPartido(id):
    json=miControladorPartido.show(id)
    return jsonify(json)

@app.route("/partido/<string:id>",methods=['PUT'])
def modificarPartido(id):
    data = request.get_json()
    json=miControladorPartido.update(id,data)
    return jsonify(json)

@app.route("/partido/<string:id>",methods=['DELETE'])
def eliminarPartido(id):
    json=miControladorPartido.delete(id)
    return jsonify(json)

@app.route("/candidato/<string:id>/partido/<string:id_partido>",methods=['PUT'])
def asignarPartidoACandidato(id,id_partido):
    json=miControladorCandidato.asignarPartido(id,id_partido)
    return jsonify(json)

#CRUD de mesa

@app.route("/mesa",methods=['GET'])
def getMesas():
    json=miControladorMesa.index()
    return jsonify(json)

@app.route("/mesa",methods=['POST'])
def crearMesa():
    data = request.get_json()
    json=miControladorMesa.create(data)
    return jsonify(json)

@app.route("/mesa/<string:id>",methods=['GET'])
def getMesa(id):
    json=miControladorMesa.show(id)
    return jsonify(json)

@app.route("/mesa/<string:id>",methods=['PUT'])
def modificarMesa(id):
    data = request.get_json()
    json=miControladorMesa.update(id,data)
    return jsonify(json)

@app.route("/mesa/<string:id>",methods=['DELETE'])
def eliminarMesa(id):
    json=miControladorMesa.delete(id)
    return jsonify(json)

#CRUD de resultado

@app.route("/resultado",methods=['GET'])
def getResultados():
    json=miControladorResultado.index()
    return jsonify(json)

@app.route("/resultado/<string:id>",methods=['GET'])
def getResultado(id):
    json=miControladorResultado.show(id)
    return jsonify(json)

@app.route("/resultado/mesa/<string:id_mesa>/candidato/<string:id_candidato>",methods=['POST'])
def crearResultado(id_mesa,id_candidato):
    data = request.get_json()
    json=miControladorResultado.create(data,id_mesa,id_candidato)
    return jsonify(json)

@app.route("/resultado/<string:id_resultado>/mesa/<string:id_mesa>/candidato/<string:id_candidato>",methods=['PUT'])
def modificarResultado(id_resultado,id_mesa,id_candidato):
    data = request.get_json()
    json=miControladorResultado.update(id_resultado,data,id_mesa,id_candidato)
    return jsonify(json)

@app.route("/resultado/<string:id_resultado>",methods=['DELETE'])
def eliminarResultado(id_resultado):
    json=miControladorResultado.delete(id_resultado)
    return jsonify(json)

#Configuracion del archivo config.json

def loadFileConfig():

    with open('config.json') as f:
        data = json.load(f)
    return data

if __name__=='__main__':
    dataConfig = loadFileConfig()
    print("Server running : "+"http://"+dataConfig["url-backend"]+":" + str(dataConfig["port"]))
    serve(app,host=dataConfig["url-backend"],port=dataConfig["port"])


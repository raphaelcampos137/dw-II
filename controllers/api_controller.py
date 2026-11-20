# Controller da API - as rotas daqui respondem DADOS em JSON.
#
#   Metodo   Endereco                 O que faz       Sucesso   Recusas
#   GET      /api/salas            lista todos     200       401
#   GET      /api/salas/<id>       devolve um      200       401 404   <- ITEM 7
#   DELETE   /api/salas/<id>       remove          204       401 404   <- ITEM 9
#
# Toda recusa tem o mesmo formato: {"erro": "mensagem"}.

from flask import Blueprint, request, session, jsonify
from models.sala import Sala
from dao.sala_dao import SalaDAO

api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.before_request
def exigir_login():
    if not session.get("usuario_id"):
        return jsonify({"erro": "Autenticacao necessaria."}), 401


@api_bp.route("/salas", methods=["GET"])
def listar():
    lista = []

    for sala in SalaDAO.listar():
        lista.append(sala.para_dicionario())

    return jsonify(lista)


@api_bp.route("/salas/<int:id>", methods=["GET"])
def buscar(id):
    sala = SalaDAO.buscar_por_id(id)

    if sala is None:
        return jsonify({"erro": "Sala nao encontrada."}), 404

    return jsonify(sala.para_dicionario()), 200


@api_bp.route("/salas/<int:id>", methods=["DELETE"])
def excluir(id):
    sala = SalaDAO.buscar_por_id(id)

    if sala is None:
        return jsonify({"erro": "Sala nao encontrada."}), 404

    SalaDAO.excluir(sala)
    return "", 204
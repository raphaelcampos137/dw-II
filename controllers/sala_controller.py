# Controller de PAGINAS - todas as rotas daqui respondem HTML ou
# redirecionamento.

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask import session
from models.sala import Sala
from dao.sala_dao import SalaDAO

sala_bp = Blueprint("sala", __name__)

@sala_bp.before_request
def verificar_login():
    if "usuario_id" not in session:
        return redirect(url_for("auth.login"))


# Listagem (GET) e cadastro (POST) na mesma rota
@sala_bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        sala = Sala(
            nome=request.form["nome"],
            bloco=request.form["bloco"],
            capacidade=request.form["capacidade"]
        )
        SalaDAO.salvar(sala)
        flash("Sala cadastrada.")
        return redirect(url_for("sala.index"))

       session["acessos"] = session.get("acessos", 0) + 1

    return render_template("index.html", salas=SalaDAO.listar())


# Edicao - GET mostra o formulario preenchido
@sala_bp.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    sala = SalaDAO.buscar_por_id(id)

    if request.method == "POST":
        SalaDAO.atualizar(
            sala,
            request.form["nome"],
            request.form["bloco"],
            request.form["capacidade"]
        )
        flash("Sala atualizada.")
        return redirect(url_for("sala.index"))

    return render_template("editar.html", sala=sala)


# Exclusao
@sala_bp.route("/excluir/<int:id>", methods=["POST"])
def excluir(id):
    sala = SalaDAO.buscar_por_id(id)
    SalaDAO.excluir(sala)
    flash("Sala excluida.")
    return redirect(url_for("sala.index"))

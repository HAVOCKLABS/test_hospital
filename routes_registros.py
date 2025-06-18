# routes_registros.py
from flask import (Blueprint, render_template, redirect,
                   url_for, flash, request)
from flask_login import login_required, current_user
from models import db, RegistroConsumo
from forms import RegistroForm

bp_registros = Blueprint("registros", __name__, url_prefix="/registros")

# ---------- Listado ----------
@bp_registros.route("/")
@login_required
def index():
    registros = RegistroConsumo.query.order_by(
        RegistroConsumo.fecha.desc(), RegistroConsumo.turno).all()
    return render_template("registros/list.html", registros=registros)

# ---------- Nuevo ----------
@bp_registros.route("/nuevo", methods=["GET", "POST"])
@login_required
def nuevo():
    form = RegistroForm()
    if form.validate_on_submit():

        # --- filtra solo los campos que existen en tu modelo ---
        data = {k: v for k, v in form.data.items()
                if k not in ("csrf_token", "submit")}

        reg = RegistroConsumo(**data, user_id=current_user.id)
        db.session.add(reg)
        db.session.commit()

        flash("Registro guardado correctamente.", "success")
        return redirect(url_for("registros.index"))

    return render_template("registros/form.html", form=form, editar=False)


# ---------- Editar ----------
@bp_registros.route("/<int:id>/editar", methods=["GET", "POST"])
@login_required
def editar(id):
    reg = RegistroConsumo.query.get_or_404(id)
    form = RegistroForm(obj=reg)
    if form.validate_on_submit():
        form.populate_obj(reg)
        db.session.commit()
        flash("Registro actualizado.", "success")
        return redirect(url_for("registros.index"))
    return render_template("registros/form.html", form=form, editar=True)

# ---------- Eliminar ----------
@bp_registros.route("/<int:id>/eliminar", methods=["POST"])
@login_required
def eliminar(id):
    reg = RegistroConsumo.query.get_or_404(id)
    db.session.delete(reg)
    db.session.commit()
    flash("Registro eliminado.", "info")
    return redirect(url_for("registros.index"))

# routes_registros.py
@bp_registros.route("/grafica")
@login_required
def grafica():
    # Obtén las lecturas ordenadas por fecha
    registros = (RegistroConsumo.query
                 .order_by(RegistroConsumo.fecha)
                 .all())

    # Prepara listas para la gráfica
    labels = [r.fecha.strftime("%d-%m-%Y") for r in registros]
    kwh    = [r.kwh_total or 0 for r in registros]
    fp     = [r.factor_potencia or 0 for r in registros]

    return render_template("registros/grafica.html",
                           labels=labels, kwh=kwh, fp=fp)

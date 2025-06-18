from flask import (
    Flask, render_template, redirect, url_for,
    request, flash, abort
)
from flask_login import (
    LoginManager, login_user, logout_user,
    login_required, current_user
)
from flask_migrate import Migrate
import json
import pandas as pd

from models import db, User, RegistroConsumo   # ← Asegúrate de tener este modelo
from routes_registros import bp_registros      # blueprint de registros

# ─── Configuración básica ──────────────────────────────────────────
app = Flask(__name__)
app.config.update(
    SECRET_KEY='19881211',
    SQLALCHEMY_DATABASE_URI='sqlite:///db.sqlite3',
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)
db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(bp_registros)

# ─── Login manager ────────────────────────────────────────────────
login_manager = LoginManager(app)
login_manager.login_view = 'login'   # redirige a /login si no autenticado

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# ─── Decorador de rol admin ───────────────────────────────────────
def admin_required(fn):
    @login_required
    def wrapper(*args, **kwargs):
        if current_user.role != 'admin':
            abort(403)
        return fn(*args, **kwargs)
    wrapper.__name__ = fn.__name__
    return wrapper

# ──────────────────────────────────────────────────────────────────
#  Función auxiliar: obtiene n días de consumo (kWh) ordenados
# ──────────────────────────────────────────────────────────────────
from datetime import date, timedelta
from sqlalchemy import func

def get_consumo_data(days: int = 7):
    """
    Devuelve listas de fechas (YYYY-MM-DD) y kWh totales diarios,
    sumando los tres turnos si existen.
    """
    # Consulta: suma kwh_total por fecha y ordena de reciente a antiguo
    rows = (
        db.session.query(
            RegistroConsumo.fecha,
            func.sum(RegistroConsumo.kwh_total).label("kwh")
        )
        .group_by(RegistroConsumo.fecha)
        .order_by(RegistroConsumo.fecha.desc())
        .limit(days)
        .all()
    )

    if rows:
        # reverse(): los ponemos en orden cronológico ascendente
        rows.reverse()
        fechas = [r.fecha.strftime("%Y-%m-%d") for r in rows]
        kwh    = [r.kwh for r in rows]        # suma diaria
    else:
        # Datos dummy si la tabla está vacía
        today = date.today()
        fechas = [(today - timedelta(days=i)).strftime("%Y-%m-%d")
                  for i in reversed(range(days))]
        kwh = [0] * days

    return fechas, kwh

# ─── Rutas públicas ───────────────────────────────────────────────
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.check_password(request.form['password']):
            login_user(user)
            flash('Sesión iniciada', 'success')
            return redirect(url_for('dashboard'))
        flash('Credenciales incorrectas', 'error')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada correctamente.', 'success')
    return redirect(url_for('login'))

# ─── Dashboard con gráfica estática ───────────────────────────────
@app.route('/')
@login_required
def dashboard():
    fechas, kwh = get_consumo_data(days=7)  # una semana
    return render_template(
        'dashboard.html',
        fechas=json.dumps(fechas),
        kwh=json.dumps(kwh)
    )

# ─── Detalle interactivo ──────────────────────────────────────────
@app.route('/grafica')
@login_required
def grafica():
    fechas, kwh = get_consumo_data(days=30)  # un mes
    return render_template(
        'grafica.html',
        fechas=json.dumps(fechas),
        kwh=json.dumps(kwh)
    )

# ─── Gestión de usuarios (solo admin) ─────────────────────────────
@app.route('/users')
@admin_required
def users():
    return render_template('users.html', users=User.query.all())

@app.route('/users/add', methods=['POST'])
@admin_required
def add_user():
    username = request.form['username'].strip()
    password = request.form['password'].strip()
    role     = request.form['role']         # 'admin' | 'registrar'

    if User.query.filter_by(username=username).first():
        flash('Nombre de usuario ocupado', 'error')
    else:
        u = User(username=username, role=role)
        u.set_password(password)
        db.session.add(u)
        db.session.commit()
        flash('Usuario creado', 'success')
    return redirect(url_for('users'))

@app.route('/users/delete/<int:user_id>', methods=['POST'])
@admin_required
def delete_user(user_id):
    if user_id == current_user.id:
        flash('No puedes eliminar tu propio usuario', 'error')
        return redirect(url_for('users'))

    u = User.query.get_or_404(user_id)
    db.session.delete(u)
    db.session.commit()
    flash('Usuario eliminado', 'success')
    return redirect(url_for('users'))

# ─── Manejadores de error ─────────────────────────────────────────
@app.errorhandler(403)
def forbidden(_):
    return render_template('404.html', msg='403 — Sin permisos'), 403

@app.errorhandler(404)
def not_found(_):
    return render_template('404.html', msg='404 — No encontrado'), 404

# ─── Punto de entrada ─────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True)   # modo desarrollo (auto-recarga y trazas)

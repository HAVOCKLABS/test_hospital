from datetime import date
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# Instancia global de SQLAlchemy (solo una)
db = SQLAlchemy()

# ---------- modelos ----------
class User(db.Model):
    id       = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role     = db.Column(db.String(20), nullable=False, default='registrar')  # 'admin' | 'registrar'

    # utilidades de contraseña
    def set_password(self, raw):
        self.password = generate_password_hash(raw)

    def check_password(self, raw):
        return check_password_hash(self.password, raw)

    # métodos requeridos por Flask-Login
    def get_id(self):
        return str(self.id)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True


class RegistroConsumo(db.Model):
    __tablename__ = "registros_consumo"

    id              = db.Column(db.Integer, primary_key=True)
    fecha           = db.Column(db.Date,  default=date.today, nullable=False)
    turno           = db.Column(db.String(12), nullable=False)   # Matutino / Vespertino / Nocturno

    # cabecera
    numero_medidor  = db.Column(db.String(20))
    multiplicador   = db.Column(db.Integer)
    hora_captura    = db.Column(db.Time)

    # conceptos del formato
    rt              = db.Column(db.Float)
    a_kwh_d         = db.Column(db.Float)
    a_max_kw_d      = db.Column(db.Float)
    time_a          = db.Column(db.Float)
    b_kwh_d         = db.Column(db.Float)
    b_max_kw_d      = db.Column(db.Float)
    time_b          = db.Column(db.Float)
    c_kwh_d         = db.Column(db.Float)
    c_max_kw_d      = db.Column(db.Float)
    time_c          = db.Column(db.Float)
    kwh_total       = db.Column(db.Float)     # código 1
    kvarh_d         = db.Column(db.Float)     # código 2
    factor_potencia = db.Column(db.Float)

    # trazabilidad
    user_id         = db.Column(db.Integer, db.ForeignKey("user.id"))

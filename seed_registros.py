"""
seed_registros.py
-----------------
Genera datos ficticios para la tabla `registros_consumo`
durante los últimos 30 días (matutino, vespertino y nocturno).
"""

import random
from datetime import date, datetime, timedelta, time

from app import app, db                         # importa tu instancia
from models import RegistroConsumo

TURNOS = {
    "Matutino":  time( 7, 30),
    "Vespertino": time(15, 30),
    "Nocturno":  time(23, 30),
}

def kwh_turno():
    """Devuelve un consumo plausible por turno."""
    base = random.uniform(150, 280)             # rango kWh por turno
    vari = random.uniform(-20,  20)             # variación aleatoria
    return round(base + vari, 2)

def seed(days: int = 30):
    hoy = date.today()
    primeros = RegistroConsumo.query.count()
    print(f"⏳ Sembrando datos… (ya existen {primeros} registros)")

    for d in range(days):
        fecha_dia = hoy - timedelta(days=d)
        for turno, hora in TURNOS.items():
            kw = kwh_turno()

            registro = RegistroConsumo(
                fecha           = fecha_dia,
                turno           = turno,
                numero_medidor  = "MD-01",
                multiplicador   = 40,
                hora_captura    = hora,

                # valores ficticios, ajusta si lo deseas
                rt              = kw * random.uniform(0.95, 1.05),
                a_kwh_d         = kw * random.uniform(0.20, 0.35),
                a_max_kw_d      = kw / 2,
                time_a          = random.uniform(0.5, 2.0),
                b_kwh_d         = kw * random.uniform(0.25, 0.40),
                b_max_kw_d      = kw / 2,
                time_b          = random.uniform(0.5, 2.0),
                c_kwh_d         = kw * random.uniform(0.20, 0.35),
                c_max_kw_d      = kw / 2,
                time_c          = random.uniform(0.5, 2.0),

                kwh_total       = kw,
                kvarh_d         = kw * random.uniform(0.3, 0.6),
                factor_potencia = random.uniform(0.85, 0.99),
            )
            db.session.add(registro)

    db.session.commit()
    total = RegistroConsumo.query.count()
    print(f"✅ Listo. Ahora hay {total} registros en total.")

if __name__ == "__main__":
    with app.app_context():        # abre contexto de aplicación
        seed(days=30)

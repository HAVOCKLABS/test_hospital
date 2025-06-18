# app/forms.py
from flask_wtf import FlaskForm
from wtforms import (DateField, TimeField, SelectField,
                     FloatField, IntegerField, SubmitField)
from wtforms.validators import DataRequired, Optional

class RegistroForm(FlaskForm):
    fecha            = DateField("Fecha", format="%Y-%m-%d",
                                 validators=[DataRequired()])
    turno            = SelectField("Turno",
                        choices=[("Matutino","Matutino"),
                                 ("Vespertino","Vespertino"),
                                 ("Nocturno","Nocturno")],
                        validators=[DataRequired()])

    numero_medidor   = IntegerField("N.º medidor",   validators=[Optional()])
    multiplicador    = IntegerField("Multiplicador", validators=[Optional()])
    hora_captura     = TimeField("Hora",             validators=[Optional()])

    rt               = FloatField("RT"         , validators=[Optional()])
    a_kwh_d          = FloatField("A KWH D"    , validators=[Optional()])
    a_max_kw_d       = FloatField("A MAX KW D" , validators=[Optional()])
    time_a           = FloatField("TIME A"     , validators=[Optional()])
    b_kwh_d          = FloatField("B KWH D"    , validators=[Optional()])
    b_max_kw_d       = FloatField("B MAX KW D" , validators=[Optional()])
    time_b           = FloatField("TIME B"     , validators=[Optional()])
    c_kwh_d          = FloatField("C KWH D"    , validators=[Optional()])
    c_max_kw_d       = FloatField("C MAX KW D" , validators=[Optional()])
    time_c           = FloatField("TIME C"     , validators=[Optional()])
    kwh_total        = FloatField("KWH D"      , validators=[Optional()])
    kvarh_d          = FloatField("KVARH D"    , validators=[Optional()])
    factor_potencia  = FloatField("Factor de potencia", validators=[Optional()])

    submit           = SubmitField("Guardar")

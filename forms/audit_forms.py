from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    FieldList,
    FloatField,
    FormField,
    IntegerField,
    SelectField,
    StringField,
    TextAreaField,
)
from wtforms.validators import DataRequired, NumberRange, Optional

from models.composant import TYPES_COMPOSANT, TYPES_INTERRUPTEUR
from models.zone import TYPES_PIECE


def _choices(values):
    return [(v, v.replace("_", " ").capitalize()) for v in values]


class ClientForm(FlaskForm):
    nom = StringField("Nom du client", validators=[DataRequired()])
    email = StringField("Email", validators=[Optional()])
    telephone = StringField("Téléphone", validators=[Optional()])
    adresse = StringField("Adresse", validators=[Optional()])
    notes = TextAreaField("Notes", validators=[Optional()])


class ProjetForm(FlaskForm):
    nom = StringField("Nom du projet", validators=[DataRequired()])
    adresse_chantier = StringField("Adresse du chantier", validators=[Optional()])
    notes = TextAreaField("Notes", validators=[Optional()])


class ComposantForm(FlaskForm):
    class Meta:
        csrf = False

    type_composant = SelectField(
        "Type de composant", choices=_choices(TYPES_COMPOSANT), validators=[DataRequired()]
    )
    type_interrupteur = SelectField(
        "Type d'interrupteur",
        choices=_choices(TYPES_INTERRUPTEUR),
        validators=[Optional()],
    )
    presence_neutre = BooleanField("Présence du neutre")
    besoin_motorisation = BooleanField("Besoin de motorisation")
    quantite = IntegerField(
        "Quantité", default=1, validators=[DataRequired(), NumberRange(min=1)]
    )
    notes = TextAreaField("Notes", validators=[Optional()])


class ZoneForm(FlaskForm):
    nom = StringField("Nom de la pièce", validators=[DataRequired()])
    type_piece = SelectField(
        "Type de pièce", choices=_choices(TYPES_PIECE), validators=[DataRequired()]
    )
    surface_m2 = FloatField("Surface (m²)", validators=[Optional()])
    notes = TextAreaField("Notes générales", validators=[Optional()])
    composants = FieldList(FormField(ComposantForm), min_entries=1)

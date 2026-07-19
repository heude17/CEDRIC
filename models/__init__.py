from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from models.client import Client  # noqa: E402,F401
from models.projet import Projet  # noqa: E402,F401
from models.zone import Zone  # noqa: E402,F401
from models.composant import Composant  # noqa: E402,F401

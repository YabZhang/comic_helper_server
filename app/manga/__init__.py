from flask import Blueprint

manga = Blueprint('manga', __name__)

from app.manga import views

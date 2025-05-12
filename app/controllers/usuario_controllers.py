from flask import Blueprint, jsonify
from app.models.filme import usuario
from app import db

usuario_bp = Blueprint('usuario', __name__)
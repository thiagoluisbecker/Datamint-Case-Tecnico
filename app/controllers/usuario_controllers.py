from flask import Blueprint, jsonify
from app.models.usuario import Usuario
from app import db

usuario_bp = Blueprint('usuario', __name__)
from flask import Blueprint, jsonify
from app.models.filme import Filme
from app import db

filme_bp = Blueprint('filme', __name__)
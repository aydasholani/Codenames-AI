# myapp/__init__.py
from flask import Flask, jsonify, session, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit, join_room, leave_room, send
from . import db_conn  # Importera din databasmodul
import os
from dotenv import load_dotenv
from .models import User, Room 
# Ladda miljövariabler
load_dotenv()

# Skapa och konfigurera SocketIO
socketio = SocketIO(logger=True, engineio_logger=True, cors_allowed_origins="*")

# En lista för att hålla reda på anslutna användare
connected_users = []

def create_app(test_config=None):
    # Skapa Flask-applikationen
    app = Flask(__name__)
    
    # Ställ in hemlig nyckel för sessionen
    app.secret_key = os.getenv("APP_SECRET_KEY")
    
    # Konfigurera databasen
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///game.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initiera SocketIO och databasanslutning med appen
    socketio.init_app(app)
    db_conn.init_app(app)
    
    # Lägg till CORS-stöd
    CORS(app)

    # Skapa en route för att få sessiondata
    @app.route('/get_session_data')
    def get_session_data():
        return jsonify({
            'room_code': session.get('room_code'),
            'username': session.get('username'),    
            'user_id': session.get('user_id')
        })
    
    # Registrera alla blueprints
    register_blueprints(app)

    return app

def register_blueprints(app):
    from .game_bp import game_bp  # Importera din blueprint
    app.register_blueprint(game_bp, url_prefix='/')

# SocketIO-händelser definieras efter `create_app`
@socketio.on('my event')
def test_message(message):
    emit('my response', {'data': message['data']})

@socketio.on('my broadcast event')
def test_message(message):
    emit('my response', {'data': message['data']}, broadcast=True)

@socketio.on('connect')
def test_connect():
    emit('my response', {'data': 'Connected'})

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

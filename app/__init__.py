from threading import Lock
from flask import Flask, jsonify, session, request, render_template, redirect, url_for
from flask_cors import CORS
from flask_socketio import SocketIO, emit, join_room, disconnect
from flask_session import Session
import os
import random
import string
from dotenv import load_dotenv
import uuid
from . import db_conn
from .models import User, Room, db
import json
load_dotenv()

async_mode = None

# Skapa och konfigurera SocketIO
socketio = SocketIO(logger=True, async_mode=async_mode, cors_allowed_origins="*", ping_interval=25, ping_timeout=60)

def create_app(test_config=None):
    app = Flask(__name__)
    
    # Ställ in hemlig nyckel för sessionen
    app.secret_key = os.getenv("APP_SECRET_KEY")
    
    # Konfigurera databasen
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///game.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db_conn.init_app(app)
    
    # Flask-Session konfiguration
    app.config['SESSION_TYPE'] = 'sqlalchemy'
    app.config['SESSION_SQLALCHEMY'] = db
    Session(app)

    # Initiera SQLAlchemy och SocketIO
    socketio.init_app(app, manage_session=False)
    
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

    # Index route
    @app.route('/')
    def index():
        return render_template('routes/index.html')
    @app.route('/waiting_room')
    def waiting_room():
        room_id = request.args.get('room_id')
        username = request.args.get('username')

        return render_template('routes/waiting_room.html', room_id=room_id, username=username)
    # Registrera alla blueprints
    # register_blueprints(app)
    
    @app.route('/create_room', methods=['POST'])
    def create_room():
        username = request.form.get('username')
        if not username:
            return "Username is required", 400

        # Generera och spara rums-ID
        room_id = generate_room_code()
        new_room = Room(id=room_id, owner_id=1)  # Använd lämplig owner_id
        db.session.add(new_room)
        db.session.commit()

        # Spara användaren och rummet i sessionen
        session['username'] = username
        session['room_id'] = room_id

        # Skapa och spara användaren i databasen
        session_id = str(uuid.uuid4())
        new_user = User(username=username, room_id=room_id, session_id=session_id)
        db.session.add(new_user)
        db.session.commit()

        # Omdirigera till waiting_room
        return redirect(url_for('routes/waiting_room', room_id=room_id))
    

    return app

def register_blueprints(app):
    from .game_bp import game_bp  # Importera din blueprint
    app.register_blueprint(game_bp, url_prefix='/')

def generate_room_code():
    """Genererar en unik 6-teckens rumskod."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

@socketio.on('create_room')
def create_room(data):
    username = data.get('username')
    if not username:
        emit('room_created', {'error': 'Username is required to create a room'})
        return

    room_id = generate_room_code()
    new_room = Room(id=room_id, owner_id=1)
    db.session.add(new_room)
    db.session.commit()

    session_id = str(uuid.uuid4())
    new_user = User(username=username, room_id=room_id, session_id=session_id)
    db.session.add(new_user)
    db.session.commit()

    join_room(room_id)
    emit('room_created', {'room_id': room_id, 'username': username, 'message': f'{username} created and joined room {room_id}'}, broadcast=True)

@socketio.on('join_room_event')
def join_room_event(data):
    username = data.get('username')
    room_id = data.get('room_id')

    if not username or not room_id:
        emit('join_error', {'error': 'Username and room ID are required'})
        return

    room = Room.query.filter_by(id=room_id).first()
    if not room:
        emit('join_error', {'error': 'Room not found'})
        return

    session_id = str(uuid.uuid4())
    new_user = User(username=username, room_id=room_id, session_id=session_id)
    db.session.add(new_user)
    db.session.commit()

    join_room(room_id)
    emit('join_success', {'room_id': room_id, 'username': username}, to=request.sid)
    emit('user_joined', {'room_id': room_id, 'username': username}, to=room_id, broadcast=True)
    
@socketio.on('connect')
def test_connect():
    emit('my response', {'data': 'Connected'})

@socketio.on('disconnect')
def handle_disconnect():
    room_id = session.get('room_code')
    username = session.get('username')
    if room_id and username:
        print(f"{username} has left room {room_id}")
        # Skicka ett meddelande till andra användare i rummet
        emit('user_left', {'username': username}, to=room_id, broadcast=True)

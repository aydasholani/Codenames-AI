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

    # Index route
    @app.route('/')
    def index():
        return render_template('routes/index.html')
    @app.route('/waiting_room')
    def waiting_room():
        room_id = request.args.get('room_id')
        username = request.args.get('username')
        
        is_owner = False
        room = Room.query.filter_by(id=room_id).first()
        if not room:
            return "Room not found", 404 
        
        current_user_id = session.get('owner_id')
        if room.owner_id == current_user_id:
            is_owner = True
            
        
        return render_template('routes/waiting_room.html', room_id=room_id, username=username, is_owner=is_owner)
    # Registrera alla blueprints
    # register_blueprints(app)
    
    @app.route('/create_room', methods=['POST'])
    def create_room():
        username = request.form.get('username')
        if not username:
            return "Username is required", 400

        # Generera och spara rums-ID

        room_id = generate_room_code()

        session_id = str(uuid.uuid4())
        # Skapa och spara användaren i databasen
        new_user = User(username=username, room_id=room_id, session_id=session_id)
        db.session.add(new_user)
        db.session.commit()
        
        # Skapa och spara rummet
        new_room = Room(id=room_id, owner_id=new_user.id)  
        db.session.add(new_room)
        db.session.commit()

        session['username'] = username
        session['room_id'] = room_id
    
     
       
        # Omdirigera till waiting_room
        return redirect(url_for('routes/waiting_room', room_id=room_id))
    

    return app

def register_blueprints(app):
    from .game_bp import game_bp  # Importera din blueprint
    app.register_blueprint(game_bp, url_prefix='/')

def generate_room_code():
    """Genererar en unik 6-teckens rumskod."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

connected_users = {}

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
    emit('room_created', {'room_id': room_id, 'username': username, 'message': f'{username} created and joined room {room_id}', 'is_owner': True}, broadcast=True)

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
    if room_id not in connected_users:
        connected_users[room_id] = []
    if username not in connected_users[room_id]:
        connected_users[room_id].append(username)

    session_id = str(uuid.uuid4())
    new_user = User(username=username, room_id=room_id, session_id=session_id)
    db.session.add(new_user)
    db.session.commit()

    join_room(room_id)
    emit('update_user_list', {'users': connected_users[room_id]}, room=room_id, broadcast=True)
    emit('join_success', {'room_id': room_id, 'username': username}, to=request.sid)
    # emit('user_joined', {'room_id': room_id, 'username': username}, to=room_id, broadcast=True)

@socketio.on('leaving_room')
def handle_leaving_room(data):
    username = data.get('username')
    room_id = data.get('room_id')

    if room_id in connected_users and username in connected_users[room_id]:
        connected_users[room_id].remove(username)
        emit('update_user_list', {'users': connected_users[room_id]}, room=room_id, broadcast=True)
        emit('user_left', {'username': username}, room=room_id, broadcast=True)
           
@socketio.on('connect')
def test_connect():
    emit('my response', {'data': 'Connected'})
    
@socketio.on('disconnect')
def handle_disconnect():
    # Här kan vi lägga logik för att hantera när en användare kopplar från
    room_id = session.get('room_code')
    username = session.get('username')

    
    if room_id and username and room_id in connected_users:
        if username in connected_users[room_id]:
            connected_users[room_id].remove(username)
            emit('update_user_list', {'users': connected_users[room_id]}, room=room_id)
            emit('user_left', {'username': username}, room=room_id)

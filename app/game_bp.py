from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
import random
import string
from . import socketio
from flask_socketio import emit
from .models import db, Room, Team, User
from uuid import uuid4

game_bp = Blueprint('game', __name__)

def generate_room_code():
    """Genererar en unik 6-teckens rumskod."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

@game_bp.route('/')
def home():
    """Startsida för att skapa eller ansluta till ett rum."""
    return render_template('routes/home.html')

@game_bp.route('/create_room', methods=['POST'])
def create_room():
    """Skapar ett nytt rum och registrerar ägaren med ett användarnamn."""
    room_code = generate_room_code()
    owner_id = random.randint(1000, 9999)
    username = request.form.get('username')  # Hämta användarnamn från formuläret

    # Skapa och spara rummet
    room = Room(id=room_code, owner_id=owner_id)
    db.session.add(room)
    db.session.commit()

    # Spara rumsinformation och användarnamn i sessionen
    session['room_code'] = room_code
    session['owner_id'] = owner_id
    session['user_id'] = str(uuid4())  # Generera ett unikt ID för användaren
    # Skapa användaren och spara i databasen
    new_user = User(username=username, room_id=room.id, session_id=session['user_id'])
    db.session.add(new_user)
    db.session.commit()

    flash(f"Rum skapades med kod: {room_code}. Du är ägare till rummet.")
    
    # Omdirigera direkt till `waiting_room`
    return redirect(url_for('game.waiting_room'))

@game_bp.route('/join_room', methods=['POST'])
def join_room_route():
    """Ansluter användare till ett rum med ett användarnamn."""
    room_code = request.form.get('room_code').upper()
    username = request.form.get('username')  # Hämta användarnamn från formuläret
    room = Room.query.filter_by(id=room_code).first()

    if room:
        # Spara rumsinformation och användarnamn i sessionen
        session['room_code'] = room_code
        session['username'] = username 
        session['user_id'] = str(uuid4())  # Generera ett unikt ID för användaren
        print(username)
        print(session['user_id'])

        # Skapa användaren och spara i databasen
        new_user = User(username=username, room_id=room_code, session_id=session['user_id'])
        
        db.session.add(new_user)
        db.session.commit()
        print(new_user.username)
        flash(f"Du har anslutit till rum {room_code}.")
        return redirect(url_for('game.waiting_room'))
    else:
        flash("Rummet existerar inte!")
        return redirect(url_for('game.home'))
 
@game_bp.route('/waiting_room')
def waiting_room():
    """Visar alla registrerade spelare och låter rumsägaren tilldela lag."""
    room_code = session.get('room_code')
    room = Room.query.filter_by(id=room_code).first()

    if not room:
        flash("Rummet kunde inte hittas.")
        return redirect(url_for('game.home'))

    # Hämta alla användare i rummet
    all_users = [user.to_dict() for user in User.query.filter_by(room_id=room_code).all()]
    username = session.get('username')
    print(all_users)
    return render_template('routes/waiting_room.html', room_code=room_code, username=username, is_owner=session.get('owner_id') == room.owner_id)    
    
# @game_bp.route('/register_user', methods=['GET', 'POST'])
# def register_user():
#     room_code = session.get('room_code')
#     room = Room.query.filter_by(id=room_code).first()
    
#     if not room:
#         flash("Rummet kunde inte hittas.")
#         return redirect(url_for('game.home'))
    
#     if request.method == 'POST':
#         username = request.form['username']
#         session_id = str(uuid4())  # Generera unikt ID
#         session['session_id'] = session_id  # Spara ID i sessionen
#         session['username'] = username  # Spara användarnamnet i sessionen
#         # Kontrollera om användaren redan är registrerad
#         existing_user = User.query.filter_by(session_id=session_id, room_id=room.id).first()
#         if not existing_user:
#             new_user = User(username=username, room_id=room.id, session_id=session_id)
#             db.session.add(new_user)
#             db.session.commit()

#             # Hämta alla användare i rummet
#             all_users = [user.to_dict() for user in User.query.filter_by(room_id=room.id).all()]
            
#             # Använd `emit` för att skicka den uppdaterade användarlistan till alla anslutna klienter i rummet
#             socketio.emit('update_user_list', {'users': all_users}, room=room_code)

#             print(f"Emitting `update_user_list` to room: {room_code} with username: {username}")
#         return redirect(url_for('game.waiting_room'))

#     return render_template('routes/register_user.html', room_code=room_code)



    # return render_template('routes/waiting_room.html', room_code=room_code, users=usernames, is_owner=session.get('owner_id') == room.owner_id)
@game_bp.route('/assign_teams', methods=['POST'])
def assign_teams():
    """Tilldelar lagfärger och agentroller."""
    room_code = session.get('room_code')
    room = Room.query.filter_by(id=room_code).first()
    users = User.query.filter_by(room_id=room.id).all()

    if not room or session.get('owner_id') != room.owner_id:
        flash("Endast rumsägaren kan tilldela lag.")
        return redirect(url_for('game.waiting_room'))

    Team.query.filter_by(room_id=room.id).delete()
    for user in users:
        user.is_agent = False

    # Skapa lag
    red_team = Team(color='röd', room_id=room.id)
    blue_team = Team(color='blå', room_id=room.id)
    db.session.add_all([red_team, blue_team])
    db.session.commit()

    random.shuffle(users)
    half = len(users) // 2
    for i, user in enumerate(users):
        user.team_id = red_team.id if i < half else blue_team.id

    # Välj agenter
    red_agent = random.choice([user for user in users if user.team_id == red_team.id])
    blue_agent = random.choice([user for user in users if user.team_id == blue_team.id])
    red_agent.is_agent = True
    blue_agent.is_agent = True

    db.session.commit()
    flash("Lagindelningen är klar och agenterna har valts.")
    return redirect(url_for('game.show_teams'))

@game_bp.route('/show_teams')
def show_teams():
    """Visar lagindelningen för användarna i rummet."""
    room_code = session.get('room_code')
    room = Room.query.filter_by(id=room_code).first()

    if not room:
        flash("Rummet kunde inte hittas.")
        return redirect(url_for('game.home'))

    red_team = Team.query.filter_by(room_id=room.id, color='röd').first()
    blue_team = Team.query.filter_by(room_id=room.id, color='blå').first()
    red_team_users = User.query.filter_by(team_id=red_team.id).all() if red_team else []
    blue_team_users = User.query.filter_by(team_id=blue_team.id).all() if blue_team else []

    return render_template('routes/show_teams.html', room_code=room_code, red_team=red_team_users, blue_team=blue_team_users, room=room)

@game_bp.route('/delete_room', methods=['POST'])
def delete_room():
    """Raderar rummet om användaren är rumsägaren."""
    room_code = session.get('room_code')
    room = Room.query.filter_by(id=room_code).first()

    if room and session.get('owner_id') == room.owner_id:
        db.session.delete(room)
        db.session.commit()
        flash("Rummet och alla associerade data har raderats.")
        session.pop('room_code', None)
        session.pop('owner_id', None)
        return redirect(url_for('game.home'))
    else:
        flash("Du har inte behörighet att radera detta rum.")
        return redirect(url_for('game.show_teams'))

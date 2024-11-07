# from flask_socketio import emit, join_room, leave_room, send
# from flask import session
# # from flask import request
# from . import socketio 
# from .model import User

# @socketio.on('join')
# def on_join(data):
#     print("data: ", data, end="\n\n")
#     username = data['username']
#     room = data['room']
#     join_room(room)
#     send(username + ' has entered the room.', to=room, broadcast=True)
    
# @socketio.on('leave')
# def on_leave(data):
#     username = data['username']
#     room = data['room']
#     leave_room(room)
#     send(username + ' has left the room.', to=room, broadcast=True)
    
# @socketio.on('connect')
# def test_connect(auth):
#     emit('my response', {'data': 'Connected'})

# @socketio.on('disconnect')
# def test_disconnect():
#     print('Client disconnected')    
    
# @socketio.on('register_user')
# def handle_register_user(data):
#     room_code = data.get('room_code')
#     username = data.get('username')
#     join_room(room_code)

#     # Skapa en lista över alla användare och skicka till rummet
#     all_users = [user.to_dict() for user in User.query.filter_by(room_id=room_code).all()]
#     print(f"Skickar 'update_waiting_list' till rum {room_code} med användare:", all_users)
#     socketio.emit('update_waiting_list', {'users': all_users}, room=room_code, broadcast=True)
     
# @socketio.on('start_round')
# def start_round(data):
#     room = data['room_code']
#     emit('round_started', {}, room=room, broadcast=True)
    
    
# @socketio.event
# def update_waiting_list(data):
#     room = data['room_code']
#     all_users = [user.to_dict() for user in User.query.filter_by(room_id=room).all()]
#     emit('update_waiting_list', {'users': all_users}, room=room, broadcast=True)
    
    



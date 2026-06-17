from flask_socketio import join_room, send, emit
from extensions import socketio, db
from app.models.chat import Message
from flask_login import current_user

@socketio.on('join')
def on_join(data):
    room = data['room']
    join_room(room)
    emit('status', {'msg': f"{current_user.username} has joined the room."}, to=room)

@socketio.on('message')
def handle_message(data):
    room = data['room']
    content = data['message']
    
    # Save to database
    new_message = Message(room_id=room, user_id=current_user.id, content=content)
    db.session.add(new_message)
    db.session.commit()
    
    emit('message', {'user': current_user.username, 'msg': content}, to=room)

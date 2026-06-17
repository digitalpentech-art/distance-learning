from flask_socketio import join_room, send, emit
from extensions import socketio, db
from app.models.chat import Message, ChatRoom
from flask_login import current_user
from app.services.chat_service import ChatService

@socketio.on('join')
def on_join(data):
    room_id = data['room']
    join_room(str(room_id))
    emit('status', {'msg': f"{current_user.username} has joined the room."}, to=str(room_id))

@socketio.on('message')
def handle_message(data):
    room_id = data['room']
    content = data['message']
    
    # Save to database using service
    new_message = ChatService.save_message(room_id, current_user.id, content)
    
    emit('message', {
        'user': current_user.username, 
        'msg': content,
        'timestamp': new_message.timestamp.strftime('%H:%M'),
        'sender_id': current_user.id
    }, to=str(room_id))

@socketio.on('typing')
def handle_typing(data):
    room_id = data['room']
    emit('display_typing', {
        'user': current_user.username,
        'is_typing': data['is_typing']
    }, to=str(room_id), include_self=False)

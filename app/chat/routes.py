from flask import render_template
from . import chat

@chat.route('/<room>')
def room(room):
    return render_template('chat/room.html', room=room)

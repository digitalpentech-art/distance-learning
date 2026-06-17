from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from . import chat
from app.models.chat import ChatRoom
from app.models.course_structure import Course
from app.services.chat_service import ChatService

@chat.route('/')
@login_required
def index():
    """List of all chat rooms for the current user."""
    rooms = current_user.chat_rooms.all()
    return render_template('chat/index.html', rooms=rooms)

@chat.route('/room/<int:room_id>')
@login_required
def room(room_id):
    """Specific chat room view."""
    room = ChatRoom.query.get_or_404(room_id)
    # Check if user is participant
    if current_user not in room.participants:
        # If group chat and student enrolled, add them
        if room.room_type == 'group' and room.course_id:
            from app.models.enrollment import Enrollment
            enrollment = Enrollment.query.filter_by(student_id=current_user.id, course_id=room.course_id).first()
            if enrollment or current_user.is_lecturer():
                ChatService.add_participant(room_id, current_user.id)
            else:
                flash("Access denied.")
                return redirect(url_for('chat.index'))
        else:
            flash("Access denied.")
            return redirect(url_for('chat.index'))
            
    return render_template('chat/room.html', room=room)

@chat.route('/course/<int:course_id>')
@login_required
def course_chat(course_id):
    """Directly enter course group chat."""
    course = Course.query.get_or_404(course_id)
    room = ChatService.get_or_create_group_chat(course_id, course.name)
    return redirect(url_for('chat.room', room_id=room.id))

@chat.route('/private/<int:user_id>')
@login_required
def private_chat(user_id):
    """Enter private chat with another user."""
    room = ChatService.get_or_create_private_chat(current_user.id, user_id)
    return redirect(url_for('chat.room', room_id=room.id))

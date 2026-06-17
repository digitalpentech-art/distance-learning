from extensions import db
from app.models.chat import ChatRoom, Message
from app.models.user import User

class ChatService:
    @staticmethod
    def get_or_create_group_chat(course_id, course_name):
        """Gets or creates a group chat for a specific course."""
        room = ChatRoom.query.filter_by(course_id=course_id, room_type='group').first()
        if not room:
            room = ChatRoom(name=f"{course_name} Group Chat", room_type='group', course_id=course_id)
            db.session.add(room)
            db.session.commit()
        return room

    @staticmethod
    def get_or_create_private_chat(user1_id, user2_id):
        """Gets or creates a private chat between two users."""
        # Find a private room where both users are participants
        user1 = User.query.get(user1_id)
        user2 = User.query.get(user2_id)
        
        # This is a bit complex in SQL, so we'll do a basic check
        rooms1 = user1.chat_rooms.filter_by(room_type='private').all()
        rooms2 = user2.chat_rooms.filter_by(room_type='private').all()
        
        common_rooms = set(rooms1).intersection(set(rooms2))
        if common_rooms:
            return list(common_rooms)[0]
        
        # Create new private room
        room_name = f"Private: {user1.username} & {user2.username}"
        room = ChatRoom(name=room_name, room_type='private')
        room.participants.append(user1)
        room.participants.append(user2)
        db.session.add(room)
        db.session.commit()
        return room

    @staticmethod
    def add_participant(room_id, user_id):
        """Adds a user to a chat room."""
        room = ChatRoom.query.get(room_id)
        user = User.query.get(user_id)
        if user not in room.participants:
            room.participants.append(user)
            db.session.commit()

    @staticmethod
    def save_message(room_id, sender_id, content):
        """Saves a chat message."""
        message = Message(room_id=room_id, sender_id=sender_id, content=content)
        db.session.add(message)
        db.session.commit()
        return message

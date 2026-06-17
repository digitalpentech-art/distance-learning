import eventlet
eventlet.monkey_patch()

# Import the app only after monkey_patching
from run import app

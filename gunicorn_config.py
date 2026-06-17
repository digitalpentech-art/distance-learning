import eventlet

def post_fork(server, worker):
    eventlet.monkey_patch()

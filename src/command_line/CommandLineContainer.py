import os

class CLIContainer(object):
    def __init__(self):
        self.address = os.getenv('SERVER_ADDR', default='127.0.0.1')
        self.port = os.getenv('SERVER_PORT', default='50051')

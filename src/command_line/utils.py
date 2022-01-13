import os 

class Utils(object):
    @staticmethod
    def project_packages(self, name: str):
            if (name == 'BigApple'):
                return [['BigPackage','1'],['markle','1']]
    
    @staticmethod
    def sample_util():
        print("Hello world!")
    
    @staticmethod
    def get_server_address():
        address = os.getenv('SERVER_ADDR', default='127.0.0.1')
        port = os.getenv('SERVER_PORT', default='50051')
        
        return [address, port] 

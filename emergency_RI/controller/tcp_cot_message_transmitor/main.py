from routing.controller import Controller
from routing.request import Request
from routing.response import Response


class TCPCoTMessageTransmitter(Controller):
    
    def __init__(self):
        pass
    
    def initialize(self, request: Request, response: Response):
        self.request = request
        self.response = response
    
    def execute(self, method=None):
        getattr(self, method)()
        return self.response
    
    def p_to_p_cot(self):
        print('sending specific cot')
    
    def broadcast_cot(self):
        print('broadcasting cot')
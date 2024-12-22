
from pycktool.model.model import Model

class Method(Model):

    def __init__(self, name: str):
        
        super().__init__(name)

        self.lloc: int = 0
        self.number_of_parameters: int = 0

class Model(object):

    def __init__(self, name: str):

        self.name: str = name

        self.called: set = set()
        self.accessed_attributes: set = set()
        self.lloc: int = 0
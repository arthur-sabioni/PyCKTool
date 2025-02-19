from pycktool.model.method_model import Method
from pycktool.model.model import Model

class Class(Model):

    def __init__(self, name: str, file: str = ''):

        super().__init__(name)
        self.file: str = file

        self.methods: dict[str, Method] = {}
        self.attributes: set = set()
        self.variables: set = set()
        self.coupled_classes: set = set()
        self.possible_coupled_classes: set = set()
        self.parents: list[Class] = list()

    def add_coupled_class(self, coupled_to: str) -> None:
        if coupled_to != self.name:
            self.coupled_classes.add(coupled_to)

    def process_possible_coupled_classes(
            self, all_classes: set, cleanup: bool = True
        ) -> None:
        """
        Process the possible coupled classes for this class.
        """
        for possible_coupled_class in self.possible_coupled_classes:
            if possible_coupled_class in all_classes:
                self.add_coupled_class(possible_coupled_class)

        if cleanup:
            self.possible_coupled_classes = set()

    def get_all_parent_names(self) -> set[str]:
        """
        Returns a set of all the names of the parent classes of this class.
        """
        return {parent.name for parent in self.parents}
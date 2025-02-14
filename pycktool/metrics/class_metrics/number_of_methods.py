from pycktool.metrics.class_metric import ClassMetric
from pycktool.model.class_model import Class

class NumberOfMethods(ClassMetric):
    
    @property
    def name(self):
        return "NOM"
    
    def calculate(self, class_obj: Class, context: dict = None) -> int:
        """
        Calculates the number of methods (NOM) for the given class.
        """
        return len(class_obj.methods.keys())
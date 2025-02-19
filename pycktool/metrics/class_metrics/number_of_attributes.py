from pycktool.metrics.class_metric import ClassMetric
from pycktool.model.class_model import Class

class NumberOfAttributes(ClassMetric):
    
    @property
    def name(self):
        return "NOA"
    
    def calculate(self, class_obj: Class, context: dict = None) -> int:
        """
        Calculates the number of attributes (NOA) for the given class.
        """
        return len(class_obj.attributes)
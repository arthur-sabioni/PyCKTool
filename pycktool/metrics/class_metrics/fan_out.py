from pycktool.metrics.class_metric import ClassMetric
from pycktool.model.class_model import Class

class FanOut(ClassMetric):
    
    @property
    def name(self):
        return "FOUT"
    
    def calculate(self, class_obj: Class, context: dict = None) -> int:
        """
        Calculates the fan out metric for the given class.

        The fan out metric is the number of classes that are dependent on the
            given class, i.e., the number of classes that the given class calls.
        """
        return len(class_obj.coupled_classes)
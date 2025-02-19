from pycktool.metrics.class_metric import ClassMetric
from pycktool.model.class_model import Class

class WeightedMethodsPerClass(ClassMetric):
    
    @property
    def name(self):
        return "WMC"
    
    def calculate(self, class_obj: Class, context: dict = None) -> int:
        """
        Calculates the weighted methods per class (WMC) of the given class.

        The weighted methods per class is the number of logical lines of code (LLOC)
            of the method divided by the total number of LLOC of the class.
        """
        return sum(method.lloc for method in class_obj.methods.values())

from pycktool.metrics.class_metric import BaseMetric
from pycktool.model.model import Model

class LogicalLinesOfCode(BaseMetric):
    
    @property
    def name(self):
        return "LLOC"
    
    def calculate(self, obj: Model, context: dict = None) -> int:
        """
        Calculates the logical lines of code (LLOC) metric for the given class.

        The LLOC metric is the number of lines of code in the class, not
            counting empty lines or lines with only whitespace.
        """
        return obj.lloc
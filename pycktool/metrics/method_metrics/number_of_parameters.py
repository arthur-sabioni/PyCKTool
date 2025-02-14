from pycktool.metrics.method_metric import MethodMetric
from pycktool.model.method_model import Method

class NumberOfParameters(MethodMetric):
    
    @property
    def name(self):
        return "NOP"
    
    def calculate(self, method_obj: Method, context: dict = None) -> int:
        """
        Calculates the number of parameters (NOP) for the given method.
        """
        return method_obj.number_of_parameters
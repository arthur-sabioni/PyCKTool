from abc import abstractmethod

from pycktool.metrics.base_metric import BaseMetric

class MethodMetric(BaseMetric):
    
    @abstractmethod
    def calculate(self, method_obj, context: dict = None):
        """
        Calculate the metric given a Method object.
        The optional context can include additional information if needed.
        """
        pass
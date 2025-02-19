from abc import abstractmethod

from pycktool.metrics.base_metric import BaseMetric

class ClassMetric(BaseMetric):
    
    @abstractmethod
    def calculate(self, class_obj, context: dict = None):
        """
        Calculate the metric given a Class object.
        The optional context can include additional information (e.g., all classes).
        """
        pass
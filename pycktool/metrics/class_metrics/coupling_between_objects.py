from pycktool.metrics.class_metric import ClassMetric
from pycktool.metrics.class_metrics.fan_in import FanIn
from pycktool.metrics.class_metrics.fan_out import FanOut
from pycktool.model.class_model import Class

class CouplingBetweenObjects(ClassMetric):
    
    @property
    def name(self):
        return "CBO"
    
    def calculate(self, class_obj: Class, context: dict = None) -> int:
        """
        Calculates the coupling between classes (CBO) metric for the given class.

        The CBO metric is computed as the Fan in + Fan out metrics.
        """
        fin = FanIn().calculate(class_obj, context)
        fout = FanOut().calculate(class_obj, context)

        return fin + fout

from pycktool.metrics.class_metric import ClassMetric
from pycktool.model.class_model import Class

class FanIn(ClassMetric):
    
    @property
    def name(self):
        return "FIN"
    
    def calculate(self, class_obj: Class, context: dict = None) -> int:
        """
        Calculates the fan in metric for the given class.

        The fan in metric is the number of classes that the given class
            depends on, i.e., the number of classes that calls the given class
        """
        all_classes: dict[str, Class] = context['all_classes']

        fan_in = 0
        for compared_class in all_classes.keys():
            if class_obj.name in all_classes[compared_class].coupled_classes:
                fan_in += 1
        return fan_in
from pycktool.metrics.class_metric import ClassMetric
from pycktool.model.class_model import Class

class NumberOfChildren(ClassMetric):
    
    @property
    def name(self):
        return "NOC"
    
    def calculate(self, class_obj: Class, context: dict = None) -> int:
        """
        Calculates the number of children (NOC) of the given class.

        The number of children is the number of classes that directly inherit 
            from the given class.
        """
        all_classes: dict[str, Class] = context['all_classes']

        noc = 0
        for class_obj in all_classes.values():
            parents = class_obj.get_all_parent_names()
            if class_obj.name in parents:
                noc += 1
        return noc
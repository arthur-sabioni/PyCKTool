from pycktool.metrics.class_metric import ClassMetric
from pycktool.model.class_model import Class

class ResponseForClass(ClassMetric):
    
    @property
    def name(self):
        return "RFC"
    
    def calculate(self, class_obj: Class, context: dict = None) -> int:
        """
        Calculates the response for class (RFC) metric for the given class.

        The RFC metric is computed as the number of methods in the class, plus
            the number of methods called by the class iself.
        """
        methods_called_by_methods = set()
        for method in class_obj.methods.values():
            methods_called_by_methods.update(method.called)
        return \
            len(class_obj.methods) + \
            len(class_obj.called)  + \
            len(methods_called_by_methods)
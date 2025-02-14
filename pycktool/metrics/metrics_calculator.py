from pycktool.metrics.base_metrics.logical_lines_of_code import LogicalLinesOfCode

from pycktool.metrics.class_metric import ClassMetric
from pycktool.metrics.class_metrics.coupling_between_objects import CouplingBetweenObjects
from pycktool.metrics.class_metrics.depth_of_inheritance_tree import DepthOfInheritanceTree
from pycktool.metrics.class_metrics.fan_in import FanIn
from pycktool.metrics.class_metrics.fan_out import FanOut
from pycktool.metrics.class_metrics.lack_of_cohesion import LackOfCohesion
from pycktool.metrics.class_metrics.number_of_attributes import NumberOfAttributes
from pycktool.metrics.class_metrics.number_of_children import NumberOfChildren
from pycktool.metrics.class_metrics.number_of_methods import NumberOfMethods
from pycktool.metrics.class_metrics.response_for_class import ResponseForClass
from pycktool.metrics.class_metrics.weighted_methods_per_class import WeightedMethodsPerClass

from pycktool.model.class_model import Class

from pycktool.metrics.method_metric import MethodMetric
from pycktool.metrics.method_metrics.number_of_parameters import NumberOfParameters


class MetricsCalculator:

    def __init__(self, classes_data: dict[str, Class]):
        """
        :param classes_data: A dictionary mapping class names to Class objects.
        """
        self.classes_data = classes_data

        # List of class metric calculators.
        self.class_metrics: list[ClassMetric] = [
            WeightedMethodsPerClass(),
            DepthOfInheritanceTree(),
            NumberOfChildren(),
            FanIn(),
            FanOut(),
            CouplingBetweenObjects(),
            ResponseForClass(),
            LackOfCohesion(),
            LogicalLinesOfCode(),
            NumberOfAttributes(),
            NumberOfMethods(),
        ]

        # List of method metric calculators.
        self.method_metrics: list[MethodMetric] = [
            LogicalLinesOfCode(),
            NumberOfParameters(),
        ]
    
    def calculate_class_metrics(self) -> dict:
        results = {}
        # context needed by some metrics.
        context = {"all_classes": self.classes_data}

        for class_name, class_obj in self.classes_data.items():
            results[class_name] = {}
            for metric in self.class_metrics:
                results[class_name][metric.name] = \
                    metric.calculate(class_obj, context)
        return results

    def calculate_method_metrics(self) -> dict:
        results = {}
        # context needed by some metrics.
        context = {}

        for class_name, class_obj in self.classes_data.items():
            results[class_name] = {}
            for method_name, method_obj in class_obj.methods.items():
                results[class_name][method_name] = {}
                for metric in self.method_metrics:
                    results[class_name][method_name][metric.name] = \
                        metric.calculate(method_obj, context)
        return results

    def calculate_all_metrics(self):
        """
        Returns a tuple with two dictionaries: class metrics and method metrics.
        """
        return self.calculate_class_metrics(), self.calculate_method_metrics()

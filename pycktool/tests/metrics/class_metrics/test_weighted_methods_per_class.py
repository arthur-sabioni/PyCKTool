import pytest

from pycktool.metrics.class_metrics.weighted_methods_per_class import WeightedMethodsPerClass
from pycktool.model.class_model import Class
from pycktool.model.method_model import Method

class TestWeightedMethodsPerClass:

    # Calculate WMC by summing LLOC of all methods in a class
    def test_wmc_correctly_sums_lloc_of_methods(self):
        # Arrange
        class_obj = Class("TestClass")
        method1 = Method("method1")
        method1.lloc = 5
        method2 = Method("method2")
        method2.lloc = 3
        class_obj.methods = {"method1": method1, "method2": method2}
        weighted_metric = WeightedMethodsPerClass()

        # Act
        result = weighted_metric.calculate(class_obj)

        # Assert
        assert result == 8

    def test_wmc_handles_empty_class(self):
        # Arrange
        class_obj = Class("TestClass")
        weighted_metric = WeightedMethodsPerClass()

        # Act
        result = weighted_metric.calculate(class_obj)

        # Assert
        assert result == 0
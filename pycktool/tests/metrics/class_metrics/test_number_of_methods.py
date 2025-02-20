import pytest

from pycktool.metrics.class_metrics.number_of_methods import NumberOfMethods
from pycktool.model.class_model import Class
from pycktool.model.method_model import Method

class TestNumberOfMethods:

    # Calculate NOM for class with multiple methods
    def test_calculate_nom_with_multiple_methods(self):
        # Arrange
        nom_metric = NumberOfMethods()
        class_obj = Class("TestClass")
        class_obj.methods = {
            "method1": Method("method1"),
            "method2": Method("method2"),
            "method3": Method("method3")
        }
    
        # Act
        result = nom_metric.calculate(class_obj)
    
        # Assert
        assert result == 3

    # Calculate NOM when methods dict is empty
    def test_calculate_nom_with_empty_methods(self):
        # Arrange
        nom_metric = NumberOfMethods()
        class_obj = Class("EmptyClass")
    
        # Act
        result = nom_metric.calculate(class_obj)
    
        # Assert
        assert result == 0
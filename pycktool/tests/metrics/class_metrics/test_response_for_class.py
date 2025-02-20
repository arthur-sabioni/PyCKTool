import pytest

from pycktool.metrics.class_metrics.response_for_class import ResponseForClass
from pycktool.model.class_model import Class
from pycktool.model.method_model import Method

class TestResponseForClass:

    # Calculate RFC for class with methods that call other methods
    def test_calculate_rfc_with_method_calls(self):
        # Arrange
        rfc_metric = ResponseForClass()
        test_class = Class("TestClass")
        method1 = Method("method1")
        method2 = Method("method2") 
        method1.called.add("external_method1")
        method1.called.add("external_method2")
        test_class.methods["method1"] = method1
        test_class.methods["method2"] = method2
        test_class.called.add("class_level_call")
    
        # Act
        result = rfc_metric.calculate(test_class)
    
        # Assert
        assert result == 5  # 2 methods + 1 class call + 2 method calls

    # Calculate RFC for class with None as methods dictionary
    def test_calculate_rfc_empty_methods(self):
        # Arrange
        rfc_metric = ResponseForClass()
        test_class = Class("TestClass")
        test_class.methods = {}
    
        # Act
        result = rfc_metric.calculate(test_class)
    
        # Assert
        assert result == 0
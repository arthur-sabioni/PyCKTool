import pytest

from pycktool.metrics.base_metrics.logical_lines_of_code import LogicalLinesOfCode
from pycktool.model.class_model import Class
from pycktool.model.method_model import Method
from pycktool.model.model import Model

class TestLogicalLinesOfCode:
    
    # Returns the logical lines of code correctly for model
    def test_returns_lloc_for_model(self):

        # Arrange
        lloc_metric = LogicalLinesOfCode()
        model = Model("test")
        model.lloc = 10

        # Act
        lloc = lloc_metric.calculate(model)

        # Assert
        assert  lloc == 10
    
    # Returns the logical lines of code correctly for Class
    def test_returns_lloc_for_class(self):

        # Arrange
        lloc_metric = LogicalLinesOfCode()
        class_obj = Class("test")
        class_obj.lloc = 10

        # Act
        lloc = lloc_metric.calculate(class_obj)

        # Assert
        assert  lloc == 10
    
    # Returns the logical lines of code correctly for Method
    def test_returns_lloc_for_method(self):

        # Arrange
        lloc_metric = LogicalLinesOfCode()
        method_obj = Method("test")
        method_obj.lloc = 10

        # Act
        lloc = lloc_metric.calculate(method_obj)

        # Assert
        assert  lloc == 10
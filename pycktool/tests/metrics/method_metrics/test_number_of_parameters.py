import pytest

from pycktool.metrics.method_metrics.number_of_parameters import NumberOfParameters
from pycktool.model.method_model import Method

class TestNumberOfParameters:

    # Return correct number of parameters for method with zero parameters
    def test_calculate_zero_parameters(self):
        method = Method("test_method")
        method.number_of_parameters = 0
    
        nop_metric = NumberOfParameters()
        result = nop_metric.calculate(method)
    
        assert result == 0

    # Return correct number of parameters for method with multiple parameters
    def test_calculate_multiple_parameters(self):
        method = Method("test_method")
        method.number_of_parameters = 3

        nop_metric = NumberOfParameters()
        result = nop_metric.calculate(method)

        assert result == 3
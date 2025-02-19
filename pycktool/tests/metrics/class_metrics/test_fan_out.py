import pytest

from pycktool.metrics.class_metrics.fan_out import FanOut
from pycktool.model.class_model import Class

class TestFanOut:

    # Calculate FOUT for a class with outgoing dependencies
    def test_fout_calculation_with_dependencies(self):
        # Arrange
        class_a = Class("ClassA")
        # Add an outgoing dependency
        class_a.coupled_classes.add("ClassB")
        fan_out_metric = FanOut()

        # Act
        result = fan_out_metric.calculate(class_a)

        # Assert
        assert result == 1

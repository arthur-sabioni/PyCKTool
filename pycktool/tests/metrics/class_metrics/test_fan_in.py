import pytest

from pycktool.metrics.class_metrics.fan_in import FanIn
from pycktool.model.class_model import Class

class TestFanIn:

    # Calculate FIN for a class with incoming dependencies
    def test_fin_calculation_with_dependencies(self):
        # Arrange
        class_a = Class("ClassA")
        class_b = Class("ClassB")
        class_c = Class("ClassC")
        # Set up coupled classes so that class_b and class_c depend on class_a.
        class_a.coupled_classes.add("ClassB")
        class_b.coupled_classes.add("ClassA")
        class_c.coupled_classes.add("ClassA")
        all_classes = {"ClassA": class_a, "ClassB": class_b, "ClassC": class_c}
        fan_in_metric = FanIn()

        # Act
        result = fan_in_metric.calculate(class_a, context={"all_classes": all_classes})

        # Assert: ClassA is in the coupled_classes of ClassB and ClassC → fan-in = 2.
        assert result == 2
import pytest

from pycktool.metrics.class_metrics.coupling_between_objects import CouplingBetweenObjects
from pycktool.model.class_model import Class

class TestCouplingBetweenObjects:
    
    # Calculate CBO for a class with both incoming and outgoing dependencies
    def test_cbo_calculation_with_dependencies(self):
        # Arrange
        class_a = Class("ClassA")
        class_b = Class("ClassB")
        class_c = Class("ClassC")
        # Add coupled classes: for CBO, FIN (incoming) + FOUT (outgoing)
        class_a.coupled_classes.add("ClassB")
        class_b.coupled_classes.add("ClassA")
        class_c.coupled_classes.add("ClassA")
        all_classes = {"ClassA": class_a, "ClassB": class_b, "ClassC": class_c}
        cbo_metric = CouplingBetweenObjects()

        # Act
        result = cbo_metric.calculate(class_a, context={"all_classes": all_classes})

        # Assert:
        assert result == 3
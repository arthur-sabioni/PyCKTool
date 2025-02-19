import pytest

from pycktool.metrics.class_metrics.number_of_children import NumberOfChildren
from pycktool.model.class_model import Class

class TestNumberOfChildren:

    # Returns 0 for a class with no child classes
    def test_noc_no_child_classes(self):
        # Arrange
        cls = Class("Class")
        all_classes = {"Class": cls}
        noc_metric = NumberOfChildren()

        # Act - pass a context with all_classes
        result = noc_metric.calculate(cls, context={"all_classes": all_classes})

        # Assert
        assert result == 0

    # Returns correct count when class has multiple direct child classes
    def test_noc_multiple_direct_child_classes(self):
        # Arrange
        parent = Class("Parent")
        child1 = Class("Child1")
        child2 = Class("Child2")
        child1.parents.append(parent)
        child2.parents.append(parent)
        all_classes = {"Parent": parent, "Child1": child1, "Child2": child2}
        noc_metric = NumberOfChildren()

        # Act
        result = noc_metric.calculate(parent, context={"all_classes": all_classes})

        # Assert
        assert result == 2
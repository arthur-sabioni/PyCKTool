import pytest

from pycktool.metrics.class_metrics.number_of_attributes import NumberOfAttributes
from pycktool.model.class_model import Class

class TestNumberOfAttributes:

    # Returns the number of attributes correctly
    def test_returns_noa_correctly(self):

        # Arrange
        noa_metrics = NumberOfAttributes()
        class_obj = Class("test")
        class_obj.attributes.add(("test", None))
        class_obj.attributes.add(("test2", None))
        class_obj.attributes.add(("test3", None))

        # Act
        noa = noa_metrics.calculate(class_obj)

        # Assert
        assert  noa == 3

    # Returns zero when there are no attributes
    def test_returns_noa_zero_when_no_attributes(self):

        # Arrange
        noa_metrics = NumberOfAttributes()
        class_obj = Class("test")

        # Act
        noa = noa_metrics.calculate(class_obj)

        # Assert
        assert  noa == 0
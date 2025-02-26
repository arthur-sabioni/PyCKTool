import pytest
from unittest.mock import MagicMock

from pycktool.metrics.metrics_calculator import MetricsCalculator
from pycktool.model.class_model import Class
from pycktool.model.method_model import Method

class TestMetricsCalculator:
    
    @pytest.fixture
    def sample_classes_data(self):
        """Creates a sample dictionary of class names mapped to Class objects with methods."""
        
        class_a = Class(name="ClassA")
        class_b = Class(name="ClassB")

        method1 = Method(name="method1")
        method2 = Method(name="method2")

        class_a.methods["method1"] = method1
        class_b.methods["method2"] = method2

        return {"ClassA": class_a, "ClassB": class_b}

    @pytest.fixture
    def metrics_calculator(self, sample_classes_data: dict[str, Class]):
        """Returns an instance of MetricsCalculator with mocked calculate methods."""
        calculator = MetricsCalculator(classes_data=sample_classes_data)

        # Mock all class metric `.calculate()` calls
        for metric in calculator.class_metrics:
            metric.calculate = MagicMock(return_value=42)

        # Mock all method metric `.calculate()` calls
        for metric in calculator.method_metrics:
            metric.calculate = MagicMock(return_value=7)

        return calculator

    def test_calculate_all_metrics_empty_classes(self):
        """
        Verifies that calling calculate_all_metrics() on an empty classes_data dictionary
        returns two empty dictionaries.
        """
        # Arrange
        metrics_calculator = MetricsCalculator({})

        # Act
        class_metrics, method_metrics = metrics_calculator.calculate_all_metrics()

        # Assert
        assert \
            len(class_metrics) == 0 and \
            len(method_metrics) == 0 and \
            isinstance(class_metrics, dict) and \
            isinstance(method_metrics, dict)

    def test_calculate_all_metrics_filled_classes(self, metrics_calculator: MetricsCalculator):
        """
        Verifies that calling calculate_all_metrics() returns two dictionaries with
        at least one key-value pair for each class and method in the given classes_data.
        """
        # Act
        class_metrics, method_metrics = metrics_calculator.calculate_all_metrics()

        # Assert
        assert \
            len(class_metrics) != 0 and \
            len(method_metrics) != 0

    def test_calculate_class_metrics_filled_classes(self, metrics_calculator: MetricsCalculator):
        """
        Verifies that calling calculate_class_metrics() returns a dictionary with
        at least one key-value pair for each class in the given classes_data.
        """
        # Act
        class_metrics = metrics_calculator.calculate_class_metrics()

        # Assert
        assert len(class_metrics) != 0

    def test_calculate_method_metrics_filled_classes(self, metrics_calculator: MetricsCalculator):
        """
        Verifies that calling calculate_method_metrics() returns a dictionary with
        at least one key-value pair for each method in the given classes_data.
        """
        
        # Act
        method_metrics = metrics_calculator.calculate_method_metrics()

        # Assert
        assert len(method_metrics) != 0
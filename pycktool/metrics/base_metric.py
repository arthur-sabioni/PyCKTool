from abc import ABC, abstractmethod

from pycktool.model.model import Model

class BaseMetric(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        """Return the metric's name (e.g., 'WMC', 'NOP')."""
        pass

    @abstractmethod
    def calculate(self, obj: Model, context: dict = None):
        """Main method to calculate metric"""
        pass
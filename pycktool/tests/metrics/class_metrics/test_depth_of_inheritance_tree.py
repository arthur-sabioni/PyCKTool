import pytest

from pycktool.metrics.class_metrics.depth_of_inheritance_tree import DepthOfInheritanceTree
from pycktool.model.class_model import Class

class TestDepthOfInheritanceTree:
    
    # Returns 0 for a class with no parent classes
    def test_dit_with_no_parents(self):
        # Arrange
        test_class = Class("TestClass")
        dit_metric = DepthOfInheritanceTree()

        # Act
        result = dit_metric.calculate(test_class)

        # Assert
        assert result == 0

    # Processes complex multiple inheritance hierarchies
    def test_dit_with_multiple_inheritance(self):
        # Arrange
        root_class = Class("RootClass")
        intermediate_class1 = Class("IntermediateClass1")
        intermediate_class2 = Class("IntermediateClass2")
        leaf_class = Class("LeafClass")
        # Set up inheritance
        intermediate_class2.parents.append(root_class)
        leaf_class.parents.extend([intermediate_class1, intermediate_class2])
        dit_metric = DepthOfInheritanceTree()

        # Act
        result = dit_metric.calculate(leaf_class)

        # Assert
        # For intermediate_class1: depth becomes 1 (no parents), and for intermediate_class2: 
        # depth becomes 1 + 1 (because of root_class) so 2. Hence, the max depth is 2.
        assert result == 2

    # Returns 1 for a class with one parent class
    def test_dit_with_one_parent(self):
        # Arrange
        parent_class = Class("ParentClass")
        child_class = Class("ChildClass")
        child_class.parents.append(parent_class)
        dit_metric = DepthOfInheritanceTree()

        # Act
        result = dit_metric.calculate(child_class)

        # Assert
        assert result == 1
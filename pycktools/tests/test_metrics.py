import pytest

from pycktools.metrics.metrics import Method, Metrics
from pycktools.model.class_model import Class

class TestMetrics:
    # Calculate WMC by summing LLOC of all methods in a class
    def test_wmc_correctly_sums_lloc_of_methods(self):
        # Arrange
        class_obj = Class("TestClass")
        method1 = Method("method1")
        method1.lloc = 5
        method2 = Method("method2") 
        method2.lloc = 3
        class_obj.methods = {"method1": method1, "method2": method2}

        # Act
        result = Metrics.wheighted_methods_per_class(class_obj)

        # Assert
        assert result == 8
        
    def test_wmc_handles_empty_class(self):
        # Arrange
        class_obj = Class("TestClass")

        # Act
        result = Metrics.wheighted_methods_per_class(class_obj)

        # Assert
        assert result == 0
        
    # Returns 0 for a class with no parent classes
    def test_dit_with_no_parents(self):
        # Arrange
        test_class = Class("TestClass")

        # Act
        result = Metrics.depth_of_inheritance_tree(test_class)

        # Assert
        assert result == 0
        
    # Processes complex multiple inheritance hierarchies
    def test_dit_with_multiple_inheritance(self):
        # Arrange
        # Create class hierarchy
        root_class = Class("RootClass")
        intermediate_class1 = Class("IntermediateClass1")
        intermediate_class2 = Class("IntermediateClass2")
        leaf_class = Class("LeafClass")
        # Set up inheritance
        intermediate_class2.parents.append(root_class)
        leaf_class.parents.extend([intermediate_class1, intermediate_class2])

        # Act
        result = Metrics.depth_of_inheritance_tree(leaf_class)

        # Assert
        assert result == 2
        
    # Returns 1 for a class with one parent class
    def test_dit_with_one_parent(self):
        # Arrange
        parent_class = Class("ParentClass")
        child_class = Class("ChildClass")
        child_class.parents.append(parent_class)

        # Act
        result = Metrics.depth_of_inheritance_tree(child_class)

        # Assert
        assert result == 1
        
    # Returns 0 for a class with no child classes
    def test_noc_no_child_classes(self):
        # Arrange
        cls = Class("Class")
        all_classes = {"Class": cls}
    
        # Act
        result = Metrics.number_of_children("Class", all_classes)
    
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

        # Act
        result = Metrics.number_of_children("Parent", all_classes)

        # Assert
        assert result == 2
        
    # Calculate CBO for a class with both incoming and outgoing dependencies
    def test_cbo_calculation_with_dependencies(self):
        # Arrange
        class_a = Class("ClassA")
        class_b = Class("ClassB") 
        class_c = Class("ClassC")
        # Add coupled classes
        class_a.coupled_classes.add("ClassB")
        class_b.coupled_classes.add("ClassA")
        class_c.coupled_classes.add("ClassA")
    
        all_classes = {
            "ClassA": class_a,
            "ClassB": class_b, 
            "ClassC": class_c
        }
    
        # Act
        cbo = Metrics.coupling_between_classes("ClassA", all_classes)
    
        # Assert - ClassA has 1 fan-in and 2 fan-out
        assert cbo == 3
        
    # Calculate FIN for a class with outgoing dependencies
    def test_fin_calculation_with_dependencies(self):
        # Arrange
        class_a = Class("ClassA")
        # Add coupled classes
        class_a.coupled_classes.add("ClassB")
    
        # Act
        fin = Metrics.fan_in(class_a)
    
        # Assert - ClassA has 2 fan-in and 1 fan-out
        assert fin == 1
        
    # Calculate FOUT for a class with incoming dependencies
    def test_fout_calculation_with_dependencies(self):
        # Arrange
        class_a = Class("ClassA")
        class_b = Class("ClassB") 
        class_c = Class("ClassC")
        # Add coupled classes
        class_a.coupled_classes.add("ClassB")
        class_b.coupled_classes.add("ClassA")
        class_c.coupled_classes.add("ClassA")
    
        all_classes = {
            "ClassA": class_a,
            "ClassB": class_b, 
            "ClassC": class_c
        }
    
        # Act
        fout = Metrics.fan_out("ClassA", all_classes)
    
        # Assert - ClassA has 1 fan-in and 2 fan-out
        assert fout == 2
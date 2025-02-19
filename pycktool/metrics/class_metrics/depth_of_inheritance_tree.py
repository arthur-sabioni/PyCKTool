from pycktool.metrics.class_metric import ClassMetric
from pycktool.model.class_model import Class

class DepthOfInheritanceTree(ClassMetric):
    
    @property
    def name(self):
        return "DIT"
    
    def calculate(self, class_obj: Class, context: dict = None) -> int:
        """
        Calculates the depth of the inheritance tree (DIT) of the given class.

        The depth is the number of superclasses until the root of the 
            inheritance tree is reached.
        """
        try:
            return self.depth_of_inheritance_tree_recursive(class_obj, 0)
        except RecursionError:
            # Maximum recursion depth exceeded. Probably a circular inheritance
            return 'Circular'
    
    def depth_of_inheritance_tree_recursive(self, class_obj: Class, depth: int) -> int:
        """
        Recursive function to calculate DIT, with an additional parameter to 
            keep track of the depth.
        """
        if len(class_obj.parents) == 0:
            return depth
        new_depth = max(
            self.depth_of_inheritance_tree_recursive(parent, depth + 1) 
            for parent in class_obj.parents
        )
        return new_depth
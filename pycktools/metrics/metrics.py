
from pycktools.model.class_model import Class
from pycktools.model.method_model import Method
from pycktools.model.model import Model


class Metrics:

    def __init__(self, classes_data: dict[str, Class]) -> None:
        self._classes_data = classes_data

    def calculate_class_metrics(self) -> dict:
        """
        Calculate metrics for each class in the dataset.

        The metrics include 
            Weighted Methods per Class (WMC)
            Depth of Inheritance Tree (DIT)
            Number of Children (NOC)
            Coupling Between Classes (CBO)
            Response for Class (RFC)
            Lack of Cohesion (LCOM)
            Fan In (FIN)
            Fan Out (FOUT)
            Logical Lines of Code (LLOC)
            Number of Attributes (NOA)
        """
        results = {}
    
        for class_name in self._classes_data.keys():
            class_data = self._classes_data[class_name]
            results[class_name] = {
                'DIT': self.depth_of_inheritance_tree(class_data),
                'NOC': self.number_of_children(class_name, self._classes_data),
                'CBO': self.coupling_between_classes(class_name, self._classes_data),
                'RFC': self.response_for_class(class_data),
                'LCOM': self.lack_of_cohesion(class_data),
                'FIN': self.fan_in(class_data),
                'FOUT': self.fan_out(class_name, self._classes_data),
                'LLOC': self.logical_lines_of_code(class_data),
                'NOA': self.number_of_attributes(class_data),
            }

        return results

    def calculate_method_metrics(self) -> dict:
        """
        Calculate metrics for each method in a class in the dataset.

        This function calculates various metrics for each class present in the 
            dataset.
        The metrics include 
            Weighted Methods per Class (WMC)
            Number of Parameters (NOP)
            Logical Lines of Code (LLOC)
        """
        results = {}
        for class_name in self._classes_data.keys():
            results[class_name] = dict()
    
        for class_name in self._classes_data.keys():
            for method in self._classes_data[class_name].methods.keys():
                method_data = self._classes_data[class_name].methods[method]
                class_data = self._classes_data[class_name]
                results[class_name][method] = {
                    'WMC': self.wheighted_methods_per_class(
                        method_data, class_data.lloc
                    ),
                    'LLOC': self.logical_lines_of_code(method_data),
                    'NOP': self.number_of_parameters(method_data),
                }

        return results

    def calculate_all_metrics(self) -> None:
        """
        Calculate all metrics for classes and methods in the dataset.

        This function calls calculate_class_metrics and calculate_method_metrics 
            to calculate all the metrics for the classes and methods in the dataset.
        """
        return self.calculate_class_metrics(), self.calculate_method_metrics()

    @staticmethod
    def wheighted_methods_per_class(class_obj: Class, class_lloc: int) -> list:
        """
        Calculates the weighted methods per class (WMC) of the given class.

        The weighted methods per class is the number of logical lines of code (LLOC)
            of the method divided by the total number of LLOC of the class.
        """
        return class_obj.lloc / class_lloc

    @staticmethod
    def depth_of_inheritance_tree(class_obj: Class) -> int:
        """
        Calculates the depth of the inheritance tree (DIT) of the given class.

        The depth is the number of superclasses until the root of the 
            inheritance tree is reached.
        """
        return Metrics.depth_of_inheritance_tree_recursive(class_obj, 0)
    
    @staticmethod
    def depth_of_inheritance_tree_recursive(class_obj: Class, depth: int) -> int:
        """
        Recursive function to calculate DIT, with an additional parameter to 
            keep track of the depth.
        """
        if len(class_obj.parents) == 0:
            return depth
        new_depth = max(
            Metrics.depth_of_inheritance_tree_recursive(parent, depth + 1) 
            for parent in class_obj.parents
        )
        return new_depth
    
    @staticmethod
    def number_of_children(class_name: str, all_classes: dict[str, Class]) -> int:
        """
        Calculates the number of children (NOC) of the given class.

        The number of children is the number of classes that directly inherit 
            from the given class.
        """
        noc = 0
        for class_obj in all_classes.values():
            parents = class_obj.get_all_parent_names()
            if class_name in parents:
                noc += 1
        return noc

    @staticmethod
    def coupling_between_classes(class_name: str, all_classes: dict[str, Class]) -> float:
        """
        Calculates the coupling between classes (CBO) metric for the given class.

        The CBO metric is computed as the Fan in + Fan out metrics.
        """
        fin = Metrics.fan_in(all_classes[class_name])
        fout = Metrics.fan_out(class_name, all_classes)

        return fin + fout

    @staticmethod
    def response_for_class(class_obj: Class) -> float:
        """
        Calculates the response for class (RFC) metric for the given class.

        The RFC metric is computed as the number of methods in the class, plus
            the number of methods called by the class iself.
        """
        methods_called_by_methods = set(
            lambda method: method.called for method in class_obj.methods.values()
        )
        return \
            len(class_obj.methods) + \
            len(class_obj.called)  + \
            len(methods_called_by_methods)

    @staticmethod
    def lack_of_cohesion(class_obj: Class) -> float:
        """
        Calculates the lack of cohesion metric (LCOM) for the given class.

        The lack of cohesion metric is computed as the number of methods in the
            class that do not access any attribute of the class, divided by the
            total number of methods in the class.
        """
        if len(class_obj.methods) == 0:
            return 0
        attributes_accessed = set()
        for method in class_obj.methods.values():
            attributes_accessed.update(method.accessed_attributes)
        return len(attributes_accessed) / len(class_obj.methods)

    @staticmethod
    def fan_in(class_obj: Class) -> float:
        """
        Calculates the fan in metric for the given class.

        The fan in metric is the number of classes that the given class
            depends on, i.e., the number of classes that calls the given class
        """
        return len(class_obj.coupled_classes)

    @staticmethod
    def fan_out(class_name: str, all_classes: dict[str, Class]) -> float:
        """
        Calculates the fan out metric for the given class.

        The fan out metric is the number of classes that are dependent on the
            given class, i.e., the number of classes that the given class calls.
        """
        fan_out = 0
        for compared_class in all_classes.keys():
            if class_name in all_classes[compared_class].coupled_classes:
                fan_out += 1
        return fan_out

    @staticmethod
    def logical_lines_of_code(obj: Model) -> int:
        """
        Calculates the logical lines of code (LLOC) metric for the given class.

        The LLOC metric is the number of lines of code in the class, not
            counting empty lines or lines with only whitespace.
        """
        return obj.lloc

    @staticmethod
    def number_of_parameters(method_obj: Method) -> int:
        """
        Calculates the number of parameters (NOP) for the given method.
        """
        return method_obj.number_of_parameters

    @staticmethod
    def number_of_attributes(class_obj: Class) -> int:
        """
        Calculates the number of attributes (NOA) for the given class.
        """
        return len(class_obj.attributes)
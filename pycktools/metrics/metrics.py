
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
            Fan In (FIN)
            Fan Out (FOUT)
            Coupling Between Objects (CBO)
            Response for Class (RFC)
            Lack of Cohesion (LCOM)
            Logical Lines of Code (LLOC)
            Number of Attributes (NOA)
            Number of Methods (NOM)
        """
        results = {}
    
        for class_name in self._classes_data.keys():
            class_data = self._classes_data[class_name]
            results[class_name] = {
                'WMC': self.wheighted_methods_per_class(class_data),
                'DIT': self.depth_of_inheritance_tree(class_data),
                'NOC': self.number_of_children(class_name, self._classes_data),
                'FIN': self.fan_in(class_name, self._classes_data),
                'FOUT': self.fan_out(class_data),
                'CBO': self.coupling_between_classes(class_name, self._classes_data),
                'RFC': self.response_for_class(class_data),
                'LCOM': self.lack_of_cohesion_4(class_data),
                'LLOC': self.logical_lines_of_code(class_data),
                'NOA': self.number_of_attributes(class_data),
                'NOM': self.number_of_methods(class_data),
            }

        return results

    def calculate_method_metrics(self) -> dict:
        """
        Calculate metrics for each method in a class in the dataset.

        This function calculates various metrics for each class present in the 
            dataset.
        The metrics include 
            Number of Parameters (NOP)
            Logical Lines of Code (LLOC)
        """
        results = {}
        for class_name in self._classes_data.keys():
            results[class_name] = dict()
    
        for class_name in self._classes_data.keys():
            for method in self._classes_data[class_name].methods.keys():
                method_data = self._classes_data[class_name].methods[method]
                results[class_name][method] = {
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
    def wheighted_methods_per_class(class_obj: Class) -> list:
        """
        Calculates the weighted methods per class (WMC) of the given class.

        The weighted methods per class is the number of logical lines of code (LLOC)
            of the method divided by the total number of LLOC of the class.
        """
        wmc = 0
        for method in class_obj.methods.values():
            wmc += method.lloc
        return wmc

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
        fin = Metrics.fan_in(class_name, all_classes)
        fout = Metrics.fan_out(all_classes[class_name])

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
    def lack_of_cohesion_4(class_obj: Class) -> float:
        """
        Calculates the lack of cohesion metric (LCOM) for the given class.

        The lack of cohesion metric is computed as the LCOM 4, resulting
        as the number of clusters of a graph where methods and attributes
        are the vertices and the dependencies between them are the edges.
        
        1 is good, 0 and >= 2 is bad.
        """
        attributes = map(lambda y: y[0], class_obj.attributes)
        methods = class_obj.methods.keys()
    
        # Instantiate vertices and edges
        vertices = list(set(attributes).union(methods))
        edges = []
        for _ in range(len(vertices)):
            edges.append([0 for _ in range(len(vertices))])
            
        # Fill edges
        for method in class_obj.methods.values():
            for attribute in method.accessed_attributes:
                if attribute in vertices:
                    edges[vertices.index(attribute)][vertices.index(method.name)] = 1
                    edges[vertices.index(method.name)][vertices.index(attribute)] = 1
            for called_method in method.called:
                if called_method in vertices:
                    edges[vertices.index(called_method)][vertices.index(method.name)] = 1
                    edges[vertices.index(method.name)][vertices.index(called_method)] = 1

        # Compute clusters
        return Metrics.count_connected_components(vertices, edges)
        
    @staticmethod
    def dfs(node, visited, edges):
        visited[node] = True
        for neighbor, is_connected in enumerate(edges[node]):
            if is_connected and not visited[neighbor]:
                Metrics.dfs(neighbor, visited, edges)

    @staticmethod
    def count_connected_components(vertices, edges):

        visited = [False] * len(vertices)
        connected_components = 0

        for node in range(len(vertices)):
            if not visited[node]:
                connected_components += 1
                Metrics.dfs(node, visited, edges)

        return connected_components


    @staticmethod
    def fan_in(class_name: str, all_classes: dict[str, Class]) -> float:
        """
        Calculates the fan in metric for the given class.

        The fan in metric is the number of classes that the given class
            depends on, i.e., the number of classes that calls the given class
        """
        fan_in = 0
        for compared_class in all_classes.keys():
            if class_name in all_classes[compared_class].coupled_classes:
                fan_in += 1
        return fan_in

    @staticmethod
    def fan_out(class_obj: Class) -> float:
        """
        Calculates the fan out metric for the given class.

        The fan out metric is the number of classes that are dependent on the
            given class, i.e., the number of classes that the given class calls.
        """
        return len(class_obj.coupled_classes)

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

    @staticmethod
    def number_of_methods(class_obj: Class) -> int:
        """
        Calculates the number of methods (NOM) for the given class.
        """
        return len(class_obj.methods.keys())
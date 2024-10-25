

class Metrics:

    def __init__(self, classes_data: dict, classes_inheritances: dict) -> None:
        self._classes_data = classes_data
        self._classes_inheritances = classes_inheritances
        pass

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
        """
        results = {}
    
        for class_name in self._classes_data.keys():
            class_data = self._classes_data[class_name]
            results[class_name] = {
                'DIT': self.depth_of_inheritance_tree(
                    class_name, self._classes_inheritances
                ),
                'NOC': self.number_of_children(
                    class_name, self._classes_inheritances
                ),
                'CBO': self.coupling_between_classes(class_data),
                'RFC': self.response_for_class(class_data),
                'LCOM': self.lack_of_cohesion(class_data),
                'FIN': self.fan_in(class_data),
                'FOUT': self.fan_out(class_data),
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
            for method in self._classes_data[class_name]['methods'].keys():
                method_data = self._classes_data[class_name]['methods'][method]
                class_data = self._classes_data[class_name]
                results[class_name][method] = {
                    'WMC': self.wheighted_methods_per_class(
                        method_data, class_data['lloc']
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
    def wheighted_methods_per_class(data: dict, class_lloc: int) -> list:
        """
        Calculates the weighted methods per class (WMC) of the given class.

        The weighted methods per class is the number of logical lines of code (LLOC)
        of the method divided by the total number of LLOC of the class.
        """
        return data['lloc'] / class_lloc

    @staticmethod
    def depth_of_inheritance_tree(class_name: str, data: dict) -> int:
        """
        Calculates the depth of the inheritance tree (DIT) of the given class.

        The depth is the number of superclasses until the root of the 
        inheritance tree is reached.
        """
        depth = 0
        current = class_name
        while current in data.keys():
            depth += 1
            current = data[current]
        return depth
    
    @staticmethod
    def number_of_children(class_name: str, data: dict) -> int:
        """
        Calculates the number of children (NOC) of the given class.

        The number of children is the number of classes that directly inherit 
            from the given class.
        """
        return len(list(filter(lambda x: x==class_name, data.values())))

    @staticmethod
    def coupling_between_classes(data: dict) -> float:
        """
        Calculates the coupling between classes (CBO) metric for the given class.

        The CBO metric is computed as the Fan in + Fan out metrics.
        """
        #Fan In + Fan Out
        #TODO: CORRIGIR
        return len(data['coupled_classes'])

    @staticmethod
    def response_for_class(data: dict) -> float:
        """
        Calculates the response for class (RFC) metric for the given class.

        The RFC metric is computed as the number of methods in the class, plus
        the number of methods called by the class iself.
        """
        methods_called_by_methods = set(
            lambda x: x['called'] for x in data['methods'].values()
        )
        return \
            len(data['methods']) + \
            len(data['called'])  + \
            len(methods_called_by_methods)

    @staticmethod
    def lack_of_cohesion(data: dict) -> float:
        """
        Calculates the lack of cohesion metric (LCOM) for the given class.

        The lack of cohesion metric is computed as the number of methods in the
        class that do not access any attribute of the class, divided by the
        total number of methods in the class.
        """
        attributes_accessed = set()
        for method in data['methods'].values():
            attributes_accessed.update(method['accessed_attributes'])
        return len(attributes_accessed) / len(data['methods'])

    @staticmethod
    def fan_in(data: dict) -> float:
        """
        Calculates the fan in metric for the given class.

        The fan in metric is the number of classes that the given class
        depends on, i.e., the number of classes that calls the given class
        """

        pass

    @staticmethod
    def fan_out(data: dict) -> float:
        """
        Calculates the fan out metric for the given class.

        The fan out metric is the number of classes that are dependent on the
        given class, i.e., the number of classes that the given class calls.
        """
        pass

    @staticmethod
    def logical_lines_of_code(data: dict) -> int:
        """
        Calculates the logical lines of code (LLOC) metric for the given class.

        The LLOC metric is the number of lines of code in the class, not
        counting empty lines or lines with only whitespace.
        """
        return data['lloc']

    @staticmethod
    def number_of_parameters(data: dict) -> int:
        return data['number_of_parameters']

    @staticmethod
    def number_of_attributes(data: dict) -> int:
        pass
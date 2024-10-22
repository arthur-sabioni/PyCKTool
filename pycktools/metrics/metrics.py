

class Metrics:

    def __init__(self, classes_data: dict, classes_inheritances: dict) -> None:
        self._classes_data = classes_data
        self._classes_inheritances = classes_inheritances
        pass

    def calculate_metrics(self) -> None:
        """
        Calculate metrics for each class in the dataset.

        This function calculates various metrics for each class present in the 
            dataset.
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
            results[class_name] = {
                'WMC': self.wheighted_methods_per_class(
                    self._classes_data[class_name]['methods']
                ),
                'DIT': self.depth_of_inheritance_tree(
                    class_name, self._classes_inheritances
                ),
                'NOC': self.number_of_children(
                    class_name, self._classes_inheritances
                ),
                'CBO': self.coupling_between_classes(
                    self._classes_data[class_name]
                ),
                'RFC': self.response_for_class(self._classes_data[class_name]),
                'LCOM': self.lack_of_cohesion(self._classes_data[class_name]),
                'FIN': self.fan_in(self._classes_data[class_name]),
                'FOUT': self.fan_out(self._classes_data[class_name]),
                'LLOC': self.logical_lines_of_code(self._classes_data[class_name]),
                'NOP': self.number_of_parameters(self._classes_data[class_name]),
                'NOA': self.number_of_attributes(self._classes_data[class_name]),
            }

        return results

    @staticmethod
    def wheighted_methods_per_class(data: dict) -> list:
        """
        Calculates the weighted methods per class (WMC) metric for the given 
            class data.

        The WMC metric is computed as the product of the logical lines of code
            (LLOC) and the number of parameters for each method. 
        It returns a list of dictionaries where each dictionary contains a 
        method name and its corresponding WMC value.
        """
        #TODO: Criar a porcentagem de linhas de código com relação ao tamanho da classe
        result = []
        for method in data.keys():
            method_wmc = \
                data[method]['lloc'] * data[method]['number_of_parameters']
            result.append({method: method_wmc})
        return result

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

        The CBO metric is computed as the number of other classes to which it is
            coupled.
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
        pass

    @staticmethod
    def fan_out(data: dict) -> float:
        pass

    @staticmethod
    def logical_lines_of_code(data: dict) -> int:
        pass

    @staticmethod
    def number_of_parameters(data: dict) -> int:
        pass

    @staticmethod
    def number_of_attributes(data: dict) -> int:
        pass
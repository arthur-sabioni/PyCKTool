from pycktool.metrics.class_metric import ClassMetric
from pycktool.model.class_model import Class

class LackOfCohesion(ClassMetric):
    
    @property
    def name(self):
        return "LCOM"
    
    def calculate(self, class_obj: Class, context: dict = None) -> int:
        """
        Calculates the lack of cohesion metric (LCOM) for the given class.

        The lack of cohesion metric is computed as the LCOM 4, resulting
        as the number of clusters of a graph where methods and attributes
        are the vertices and the dependencies between them are the edges.
        
        1 is good, 0 and >= 2 is bad.
        """
        attributes = map(lambda y: y[0], class_obj.attributes)
        methods = class_obj.methods.keys()

        if len(methods) == 0 or \
           len(methods) == 1 and list(methods)[0] == '__init__':
            return 0
    
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
        return self.count_connected_components(edges)

    def count_connected_components(self, edges):

        visited = [False] * len(edges)
        connected_components = 0

        for node in range(len(edges)):
            if not visited[node]:
                connected_components += 1
                self.dfs(node, visited, edges)

        return connected_components
        
    @staticmethod
    def dfs(node, visited, edges):
        visited[node] = True
        for neighbor, is_connected in enumerate(edges[node]):
            if is_connected and not visited[neighbor]:
                LackOfCohesion.dfs(neighbor, visited, edges)
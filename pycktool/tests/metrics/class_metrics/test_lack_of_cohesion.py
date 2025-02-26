import pytest

from pycktool.metrics.class_metrics.lack_of_cohesion import LackOfCohesion
from pycktool.model.class_model import Class
from pycktool.model.method_model import Method

class TestLackOfCohesion:

    @pytest.fixture
    def lcom_metric(self):
        return LackOfCohesion()

    def test_lcom_no_methods(self, lcom_metric: LackOfCohesion):
        # Arrange
        class_obj = Class('test')
        
        # Act
        result = lcom_metric.calculate(class_obj)
        
        # Assert
        assert result == 0

    def test_lcom_only_init_method(self, lcom_metric: LackOfCohesion):
        # Arrange
        class_obj = Class('test')
        class_obj.methods['__init__'] = Method('__init__')
        
        # Act
        result = lcom_metric.calculate(class_obj)
        
        # Assert
        assert result == 0

    def test_lcom_multiple_methods_disconnected(self, lcom_metric: LackOfCohesion):
        # Arrange
        class_obj = Class('test')
        class_obj.methods['method1'] = Method('method1')
        class_obj.methods['method2'] = Method('method2')
        
        # Act
        result = lcom_metric.calculate(class_obj)
        
        # Assert
        assert result == 2

    def test_lcom_multiple_methods_with_dependencies(self, lcom_metric: LackOfCohesion):
        # Arrange
        class_obj = Class('test')
        method1 = Method('method1')
        method1.called = ['method2']
        class_obj.methods['method1'] = method1
        method2 = Method('method2')
        method2.called = ['method1']
        class_obj.methods['method2'] = method2
        
        # Act
        result = lcom_metric.calculate(class_obj)
        
        # Assert
        assert result == 1

    def test_lcom_multiple_methods_with_dependencies_and_attributes(self, lcom_metric: LackOfCohesion):
        # Arrange
        class_obj = Class('test')
        class_obj.attributes = [('attr1', None), ('attr2', None)]
        method1 = Method('method1')
        method1.accessed_attributes = ['attr1']
        method1.called = ['method2']
        class_obj.methods['method1'] = method1
        method2 = Method('method2')
        method2.accessed_attributes = ['attr2']
        method2.called = ['method1']
        class_obj.methods['method2'] = method2
        
        # Act
        result = lcom_metric.calculate(class_obj)
        
        # Assert
        assert result == 1

    def test_count_empty_graph_returns_node_count(self):
        # Arrange
        edges = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

        # Act
        result = LackOfCohesion.count_connected_components(edges)

        # Assert
        assert result == 3

    # Single connected component in graph returns 1
    def test_count_single_connected_component_returns_one(self):
        # Arrange
        edges = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]

        # Act
        result = LackOfCohesion.count_connected_components(edges)

        # Assert
        assert result == 1

    # Multiple separate components return correct count
    def test_count_multiple_separate_components(self):
        # Arrange
        edges = [
            [0, 1, 0, 0],
            [1, 0, 0, 0],
            [0, 0, 0, 1],
            [0, 0, 1, 0]
        ]

        # Act
        result = LackOfCohesion.count_connected_components(edges)

        # Assert
        assert result == 2

    # DFS traverses all connected nodes in a graph starting from given node
    def test_dfs_traverses_connected_nodes(self):
        # Graph with 4 nodes where 0->1->2->3 form a path
        edges = [
            [0, 1, 0, 0],
            [0, 0, 1, 0], 
            [0, 0, 0, 1],
            [0, 0, 0, 0]
        ]
        visited = [False] * 4
    
        LackOfCohesion.dfs(0, visited, edges)
    
        assert all(visited) == True

    # Graph with no edges (isolated nodes)
    def test_dfs_isolated_nodes(self):
        # Graph with 3 isolated nodes (no edges)
        edges = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]
        visited = [False] * 3
    
        LackOfCohesion.dfs(0, visited, edges)
    
        assert visited == [True, False, False]

        # Method processes all neighbors of current node
    def test_dfs_processes_all_neighbors(self):
        # Graph with 3 nodes where 0 is connected to 1 and 2
        edges = [
            [0, 0, 0],
            [0, 0, 1],
            [0, 1, 0]
        ]
        visited = [False] * 3

        LackOfCohesion.dfs(1, visited, edges)

        assert visited == [False, True, True]
import pytest
from pycktools.parser.code_parser import CodeParser

class TestCodeParser:

    _FULL_CODE =  """
    class UsedClass6:
        def __init__(self):
            pass

    class UsedClassWithConst:
        USED_CONST = 'I am here to be used!'

        def __init__(self):
            pass
                                
    class UsedClass:
        def __init__(self):
                self.used_attr_1 = 'I am here to be used!'
                self.used_attr_2 = 'I am here to be used!'
                self.used_attr_3 = UsedClass()
        
    class MySuperParent:
        super_parent_var = 0

        def __init__(self):
            pass
            
    class MyParent(MySuperParent1, MySuperParent2):
        parent_var = 0

        def __init__(self):
            pass

    class MyClass(MyParent):
        class_variable = UsedClass6()

        def __init__(self, value: str):
            self.instance_variable = value
            self.UsedClassAttribute = UsedClass8()
            self.instance_from_const = UsedClassWithConst.USED_CONST
            usedClassVariable = UsedClass()
            UsedClassMethod1.used_method()
            tmp = UsedClassMethod2.used_method()

        def my_method(self):
            print(self.instance_variable)
            print(self.UsedClassAttribute.used_attr)
            print(self.UsedClassAttribute.used_attr_2, self.UsedClassAttribute.used_attr_3)

    def my_function():
        local_variable = 10
        print(local_variable)
    """

    @pytest.fixture
    def parsed_full_code(self):
        cp = CodeParser()
        cp.extract_code_data(self._FULL_CODE)
        yield cp

    def test_full_code_parsed_all_classes(self, parsed_full_code: CodeParser):
        assert len(parsed_full_code.classes) == 8

    def test_full_code_parsed_all_methods(self, parsed_full_code: CodeParser):
        """
        This test verifies that the code parser is able to extract all the methods present in the code.
        It should extract 8 methods from the full code.
        """
        methods_per_class = list(map(lambda x: x.methods.keys(), parsed_full_code.classes.values()))
        counted_methods = sum(len(x) for x in methods_per_class)
        assert counted_methods == 7

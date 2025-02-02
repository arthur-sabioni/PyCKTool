import pytest
from pycktool.parser.code_parser import CodeParser

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

    @pytest.mark.parametrize(
        'code', [
            ("""
                    if self._used_attribute:
                        pass
            """),
            ("""
                    if not True and not self._used_attribute:
                        pass
            """),
            ("""
                    if condition:
                        var = self._used_attribute
            """),
            ("""
                    if condition:
                        pass
                    else:
                        var = self._used_attribute
            """),
            ("""
                    if condition:
                        pass
                    elif condition:
                        function_call()
                        var = self._used_attribute
                    else:
                        pass
            """),
            ("""
                    for _ in range(1):
                        var = self._used_attribute
            """),
            ("""
                    for _ in range(1):
                        self._used_attribute = 0
            """),
            ("""
                    for _ in range(1):
                        if condition:
                            self._used_attribute = 0
            """),
            ("""
                    while True:
                        if condition:
                            self._used_attribute = 0
            """),
            ("self._used_attribute.add('foo')"),
            ("return self._used_attribute"),
            ("return '', self._used_attribute"),
            ("return {foo.name for foo in self._used_attribute}")
        
        ]
    )
    def test_code_parser_gets_accessed_attriutes_correctly(self, code: str):
        test_code = f"""
            class Test:
                def test_function(self):
                    {code}
        """
        cp = CodeParser()
        cp.extract_code_data(test_code)
        assert "_used_attribute" in \
            cp.classes["Test"].methods["test_function"].accessed_attributes
    
    @pytest.mark.parametrize(
        'code', [
            ("""
                        if condition:
                            self.called_function()
            """),
            ("""
                        if condition:
                            pass
                        else:
                            self.called_function()
            """),
            ("""
                        if condition:
                            pass
                        elif condition:
                            var = self._used_attribute
                            self.called_function()
                        else:
                            pass
            """),
            ("""
                        if condition:
                            pass
                        elif condition:
                            pass
                        else:
                            self.called_function()
            """),
            ("""
                        for _ in range(1):
                            var = self.called_function()
            """),
            ("""
                        for _ in range(1):
                            self.called_function()
            """),
            ("""
                        for _ in range(1):
                            if condition:
                                self.called_function()
            """),
            ("""
                        while True:
                            if condition:
                                self.called_function()
            """),
            ("""
                        return self.called_function()
            """),
            ("""
                        return '',self.called_function()
            """),
            ("""
                        if not true and not self.called_function():
                            pass
            """),
            ("""
                        try:
                            foo = self.called_function()
                        except:
                            pass
            """),
            ("""
                        try:
                            pass
                        except:
                            self.called_function()
            """)
        ]
    )
    def test_code_parser_gets_self_calls_correctly(self, code: str):
        test_code = f"""
            class Test:
                def test_function(self):
                    {code}
        """
        cp = CodeParser()
        cp.extract_code_data(test_code)
        assert "called_function" in \
            cp.classes["Test"].methods["test_function"].called
    
    @pytest.mark.parametrize(
        'code', [
            ("""
                    def test_function(self, parameter: CoupledClass):
                        if condition:
                            self.called_function()
            """),
            ("""
                    def test_function(self, parameter: Dummy | CoupledClass | Dummy):
                        if condition:
                            self.called_function()
            """),
        ]
    )
    def test_code_parser_gets_coupling_correctly(self, code: str):
        test_code = f"""
            class Test:
                {code}
        """
        cp = CodeParser()
        cp.extract_code_data(test_code)
        assert "CoupledClass" in \
            cp.classes["Test"].possible_coupled_classes

    @pytest.mark.parametrize(
        'code,function_name', [
            # ("""
            #             self._attribute.add('foo')
            # """, '_attribute.add'),
            ("""
                        max([1,2,3])
            """, 'max'),
            ("""
                        set([1,2,3])
            """, 'set'),
            ("""
                        map([1,2,3])
            """, 'map'),
            ("""
                        enumerate([1,2,3])
            """, 'enumerate'),
            # ("""
            #             foo.append('bar')
            # """, 'foo.append'),
            # ("""
            #             foo.keys()
            # """, 'foo.keys'),
        ]
    )
    def test_code_parser_ignores_called_built_in_functions(self, code:str, function_name: str):
        test_code = f"""
            class Test:
                def test_function(self):
                    {code}
        """
        cp = CodeParser()
        cp.extract_code_data(test_code)
        assert function_name not in \
            cp.classes["Test"].methods["test_function"].called

    def test_code_parser_ignores_built_in_inheritances(self):
        test_code = f"""
            class Test(str):
                pass
        """
        cp = CodeParser()
        cp.extract_code_data(test_code)
        assert 'str' not in \
            cp.classes["Test"].coupled_classes
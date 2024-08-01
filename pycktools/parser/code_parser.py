import astroid

class CodeParser:
    
    _CLASS_INIT = {
        'methods': [],
        'attributes': set(),
        'children': 0,
        'depth': 0,
        'coupled_classes': set()
    }
    
    def __init__(self, code: str) -> None:
        
        self.code = code
        
        self.classes = {}
        self.methods = {}
        self.inheritances = {}
        
    def get_class(self, class_name) -> dict:
        
        return self.classes.get(class_name, self._CLASS_INIT)
        
    def extract_function(self, node: astroid.FunctionDef, class_name: str) -> None:
        
        method_name = node.name
        self.classes[class_name]['methods'].append(method_name)
        self.methods[method_name] = {
            'accessed_attributes': set(),
            'called_methods': set()
        }
        
        for method_node in node.body:
            if isinstance(method_node, astroid.Assign):
                for target in method_node.targets:
                    if isinstance(target, astroid.Attribute):
                        attr_name = target.attrname
                        self.classes[class_name]['attributes'].add(attr_name)
                        self.methods[method_name]['accessed_attributes'].add(attr_name)
            
            elif isinstance(method_node, astroid.Expr):
                if isinstance(method_node.value, astroid.Call):
                    called_method = method_node.value.func.as_string()
                    self.methods[method_name]['called_methods'].add(called_method)
                    if '.' in called_method:
                        callee_class = called_method.split('.')[0]
                        if callee_class != class_name:
                            self.classes[class_name]['coupled_classes'].add(callee_class)
                            
    def extract_inheritance(self, base: astroid.FunctionDef, class_name: str) -> None:
        base_class = base.name
        self.inheritances[class_name] = base_class
        if base_class in self.classes:
            self.classes[base_class]['children'] += 1

    def extract_classes_and_methods(self) -> None:
        
        module = astroid.parse(self.code)

        for node in module.body:
            if isinstance(node, astroid.ClassDef):
                class_name = node.name
                self.classes[class_name] = {
                    'methods': [],
                    'attributes': set(),
                    'children': 0,
                    'depth': 0,
                    'coupled_classes': set()
                }

                # Extract methods and attributes
                for class_node in node.body:
                    if isinstance(class_node, astroid.FunctionDef):
                        self.extract_function(class_node, class_name)

                # Extract inheritance information
                for base in node.bases:
                    if isinstance(base, astroid.Name):
                        self.extract_inheritance(base, class_name)


# Test execution
if __name__ == "__main__":
    cp = CodeParser("""
        class MySuperParent:
            super_parent_var = 0

            def __init__(self):
                pass
                
        class MyParent(MySuperParent):
            parent_var = 0

            def __init__(self):
                pass

        class MyClass(MyParent):
            class_variable = 0

            def __init__(self, value):
                self.instance_variable = value

            def my_method(self):
                print(self.instance_variable)

        def my_function():
            local_variable = 10
            print(local_variable)
    """)
    cp.extract_classes_and_methods()
    
    print('')

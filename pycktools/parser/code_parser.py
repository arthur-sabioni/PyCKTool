import astroid
import json

class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)

class CodeParser:
    
    def __init__(self) -> None:

        self.classes = {}
        self.methods = {}
        self.inheritances = {}
        
    def get_class(self, class_name) -> dict:
        
        return self.classes.get(class_name, self._CLASS_INIT)

    def count_lloc(self, node):
        """
        Count the number of logical lines of code in the given AST node.
        """
        if not isinstance(node, (astroid.FunctionDef, astroid.AsyncFunctionDef)):
            raise ValueError("Node must be a function or method definition")
        
        lloc = 0
        for child in node.body:
            if isinstance(child, (astroid.Assign, astroid.AugAssign, astroid.AnnAssign, astroid.Expr, astroid.Return,
                                astroid.Raise, astroid.Delete, astroid.Pass, astroid.Break, astroid.Continue,
                                astroid.Global, astroid.Nonlocal, astroid.Assert, astroid.Import, astroid.ImportFrom)):
                lloc += 1
            elif isinstance(child, (astroid.If, astroid.For, astroid.While, astroid.Try, astroid.With)):
                lloc += self.count_lloc_in_compound_statement(child)
        return lloc

    def count_lloc_in_compound_statement(self, node):
        """
        Recursively count the logical lines of code in compound statements like if, for, while, try, with.
        """
        lloc = 1  # Count the compound statement itself
        for child in node.body:
            if isinstance(child, (astroid.Assign, astroid.AugAssign, astroid.AnnAssign, astroid.Expr, astroid.Return,
                                astroid.Raise, astroid.Delete, astroid.Pass, astroid.Break, astroid.Continue,
                                astroid.Global, astroid.Nonlocal, astroid.Assert, astroid.Import, astroid.ImportFrom)):
                lloc += 1
            elif isinstance(child, (astroid.If, astroid.For, astroid.While, astroid.Try, astroid.With)):
                lloc += self.count_lloc_in_compound_statement(child)
        for child in getattr(node, 'orelse', []):
            if isinstance(child, (astroid.Assign, astroid.AugAssign, astroid.AnnAssign, astroid.Expr, astroid.Return,
                                astroid.Raise, astroid.Delete, astroid.Pass, astroid.Break, astroid.Continue,
                                astroid.Global, astroid.Nonlocal, astroid.Assert, astroid.Import, astroid.ImportFrom)):
                lloc += 1
            elif isinstance(child, (astroid.If, astroid.For, astroid.While, astroid.Try, astroid.With)):
                lloc += self.count_lloc_in_compound_statement(child)
        return lloc
    
    def extract_attributes_recursive(self, node, dict, class_name) -> None:
        if isinstance(node.value, astroid.Call):
            if node.value.args:
                for arg in node.value.args:
                    self.extract_attributes_recursive(arg, dict, class_name)
            called_method = node.value.func.as_string()
            node['called_methods'].add(called_method)
            if '.' in called_method:
                callee_class = called_method.split('.')[0]
                if callee_class != class_name:
                    self.classes[class_name]['coupled_classes'].add(callee_class)
        
    def extract_methods(self, node: astroid.FunctionDef, class_name: str) -> None:
        
        method_name = node.name
        method_dict = {
            'accessed_attributes': set(),
            'called_methods': set(),
            'lloc': self.count_lloc(node),
            'number_of_parameters': len(node.args.args),
        }
        
        for method_node in node.body:
            if isinstance(method_node, astroid.Assign):
                for target in method_node.targets:
                    if isinstance(target, astroid.AssignAttr):
                        attr_name = target.attrname
                        self.classes[class_name]['attributes'].add(attr_name)
                        method_dict['accessed_attributes'].add(attr_name)
            
            elif isinstance(method_node, astroid.Expr):
                # self.extract_attributes_recursive(method_node, method_dict, class_name)
                if isinstance(method_node.value, astroid.Call):
                    if method_node.value.args:
                        for arg in method_node.value.args:
                            arg_string = arg.as_string().replace('self.', '')
                            if '.' in arg_string:
                                callee_class = arg_string.split('.')[0]
                                if callee_class != class_name:
                                    self.classes[class_name]['coupled_classes'].add(callee_class)
                            method_dict['accessed_attributes'].add(arg_string)
                    called_method = method_node.value.func.as_string().replace('self.', '')
                    method_dict['called_methods'].add(called_method)
                    if '.' in called_method:
                        callee_class = called_method.split('.')[0]
                        if callee_class != class_name:
                            self.classes[class_name]['coupled_classes'].add(callee_class)

        self.classes[class_name]['methods'][method_name] = method_dict
                            
    def extract_inheritance(self, base: astroid.FunctionDef, class_name: str) -> None:
        base_class = base.name
        self.inheritances[class_name] = base_class
        if base_class in self.classes:
            self.classes[base_class]['direct_children'] += 1

    def extract_classes_and_methods(self, code: str) -> None:
        
        module = astroid.parse(code)

        for node in module.body:
            if isinstance(node, astroid.ClassDef):
                class_name = node.name
                self.classes[class_name] = {
                    'methods': {},
                    'attributes': set(),
                    'variables': set(),
                    'direct_children': 0,
                    'coupled_classes': set()
                }

                # Extract methods and attributes
                for class_node in node.body:
                    if isinstance(class_node, astroid.FunctionDef):
                        self.extract_methods(class_node, class_name)

                    elif isinstance(class_node, astroid.Assign):
                        for target in class_node.targets:
                            attr_name = target.name
                            self.classes[class_name]['variables'].add(attr_name)

                # Extract inheritance information
                for base in node.bases:
                    if isinstance(base, astroid.Name):
                        self.extract_inheritance(base, class_name)


# Test execution
if __name__ == "__main__":
    cp = CodeParser()
    cp.extract_classes_and_methods(r"""
                                   
        class UsedClass:
            def __init__(self):
                self.used_attr_1 = 'I am here to be used!'
                self.used_attr_2 = 'I am here to be used!'
                self.used_attr_3 = 'I am here to be used!'
        
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
                self.UsedClass = UsedClass()

            def my_method(self):
                print(self.instance_variable)
                print(self.UsedClass.used_attr)
                print(self.UsedClass.used_attr_2, self.UsedClass.used_attr_3)

        def my_function():
            local_variable = 10
            print(local_variable)

    """)
    
    print('')
    print(json.dumps(cp.classes, cls=SetEncoder))
    print(json.dumps(cp.inheritances, cls=SetEncoder))
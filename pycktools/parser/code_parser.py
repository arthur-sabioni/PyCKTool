import astroid

from pycktools.model.class_model import Class
from pycktools.model.method_model import Method
from pycktools.model.model import Model

class CodeParser:
    
    def __init__(self) -> None:

        self.classes: dict[str, Class] = {}

    def _get_class(self, class_name: str) -> Class:
        """
        Gets a class from the classes dictionary, or creates a new class if not 
            found.
        """
        return self.classes.get(class_name, Class(class_name))

    def count_lloc(self, node):
        """
        Count the number of logical lines of code in the given AST node.
        """
        if not isinstance(node, (
            astroid.FunctionDef, astroid.AsyncFunctionDef, astroid.ClassDef
        )):
            raise ValueError("Node must be a function or method definition")
        
        lloc = 0
        for child in node.body:
            if isinstance(child, (
                astroid.Assign, astroid.AugAssign, astroid.AnnAssign, astroid.Expr, astroid.Return,
                astroid.Raise, astroid.Delete, astroid.Pass, astroid.Break, astroid.Continue,
                astroid.Global, astroid.Nonlocal, astroid.Assert, astroid.Import, astroid.ImportFrom
            )):
                lloc += 1
            elif isinstance(child, (astroid.If, astroid.For, astroid.While, astroid.Try, astroid.With)):
                lloc += self.count_lloc_in_compound_statement(child)
            elif isinstance(child, (astroid.FunctionDef, astroid.AsyncFunctionDef)):
                lloc += 1 + self.count_lloc(child)
        return lloc

    def count_lloc_in_compound_statement(self, node):
        """
        Recursively count the logical lines of code in compound statements like if, for, while, try, with.
        """
        lloc = 1  # Count the compound statement itself
        for child in node.body:
            if isinstance(child, (
                astroid.Assign, astroid.AugAssign, astroid.AnnAssign, astroid.Expr, astroid.Return,
                astroid.Raise, astroid.Delete, astroid.Pass, astroid.Break, astroid.Continue,
                astroid.Global, astroid.Nonlocal, astroid.Assert, astroid.Import, astroid.ImportFrom
            )):
                lloc += 1
            elif isinstance(child, (astroid.If, astroid.For, astroid.While, astroid.Try, astroid.With)):
                lloc += self.count_lloc_in_compound_statement(child)
        for child in getattr(node, 'orelse', []):
            if isinstance(child, (
                astroid.Assign, astroid.AugAssign, astroid.AnnAssign, astroid.Expr, astroid.Return,
                astroid.Raise, astroid.Delete, astroid.Pass, astroid.Break, astroid.Continue,
                astroid.Global, astroid.Nonlocal, astroid.Assert, astroid.Import, astroid.ImportFrom
            )):
                lloc += 1
            elif isinstance(child, (astroid.If, astroid.For, astroid.While, astroid.Try, astroid.With)):
                lloc += self.count_lloc_in_compound_statement(child)
        return lloc
    
    def _is_built_in(self, node: astroid.NodeNG) -> bool:
        """
        Determines if the given node is part of a built-in module.
        """
        return node.root().name in {"builtins", "__builtin__"}

    def _extract_coupled_classes(self, node: astroid.Name, class_name: str) -> None:
        """
        Tries to infer a class constructor from the given node and add it as a
        coupled class of the given class name. If it could not infer, it adds
        the node name as a possible coupled class to be processed later.
        """
        if isinstance(node, astroid.Name):
            try:
                inferred = next(node.infer(), None)
                if inferred is astroid.Uninferable:
                    raise Exception
                if isinstance(inferred, astroid.ClassDef):
                    if not self._is_built_in(inferred):
                        self.classes[class_name].add_coupled_class(inferred.name)
            except:
                # If could not infer, try to detect it at post processing
                self.classes[class_name].possible_coupled_classes.add(node.name)
    
    def _extract_used_attributes_recursive(
        self, node, obj: Model, class_name
    ) -> None:
        """
        Recursively traverse the node and extract the methods that are called 
            and the attributes that are accessed. 
        The extracted data is stored in the given dictionary.
        """
        if isinstance(node, astroid.Call):
            if node.args:
                for arg in node.args:
                    self._extract_used_attributes_recursive(arg, obj, class_name)
            called_method = node.func.as_string()
            obj.called.add(called_method)

            self._extract_coupled_classes(node.func, class_name)

            # Checking if call is a Class method
            if '.' in called_method:
                if getattr(node.func, "expr", None):
                    self._extract_coupled_classes(node.func.expr, class_name)

        if isinstance(node, astroid.Attribute):
            attr_name = node.attrname
            if 'self' not in node.expr.as_string():
                used_class = node.expr.as_string()
                attr_name = used_class + '.' + attr_name
            obj.accessed_attributes.add(attr_name)

    def _extract_self_attributes(self, node, obj: Model, class_name) -> None:
        """
        Extract the attributes of the class that are accessed via the 'self' 
            variablefrom the given node and store the extracted data in the 
            given dictionary.
        """
        for target in node.targets:
            if isinstance(target, astroid.AssignAttr):
                attr_name = target.attrname
                try:
                    attr_instance = next(target.infer(), None).pytype()
                    if attr_instance is astroid.Uninferable:
                        attr_instance = None
                    else:
                        if attr_instance[0] == '.':
                            attr_instance = attr_instance[1:]
                except:
                    attr_instance = None
                self.classes[class_name].attributes.add((
                    attr_name, attr_instance
                ))
                obj.accessed_attributes.add(attr_name)
        
    def _extract_methods(
        self, node: astroid.FunctionDef, class_name: str
    ) -> None:
        """
        Extract the methods of the class from the given node and store the 
            extracted data in the classes dictionary.

        The extracted data includes the name of the method, the logical lines of 
            code (LLOC), the number of parameters, the attributes that are 
            accessed and the methods that are called.
        """
        method_name = node.name
        method_obj = Method(method_name)
        method_obj.lloc = self.count_lloc(node)
        method_obj.number_of_parameters = len(node.args.args)

        # Add parameters types to possible coupled classes
        for typing in node.args.annotations:
            if isinstance(typing, astroid.Name) and not self._is_built_in(typing):
                self.classes[class_name].possible_coupled_classes.add(typing.name)

        # Add return type to possible coupled classes
        if node.returns:
            self._extract_return_type(node.returns, class_name)
        
        for method_node in node.body:
            self._extract_methods_data_recursively(method_node, method_obj, class_name)

        self.classes[class_name].methods[method_name] = method_obj

    def _extract_methods_data_recursively(
            self, node, method_obj: Method, class_name: str
        ) -> None:
        """
        Recursively traverse the given method node and extract the methods that
            are called and the attributes that are accessed.
        """
        if isinstance(node, astroid.Assign):
            self._extract_self_attributes(node, method_obj, class_name)
        
        if isinstance(node, (astroid.Expr, astroid.Assign)):
            self._extract_used_attributes_recursive(
                node.value, method_obj, class_name
            )

        # If this method node has a body, traverse through it.
        if hasattr(node, 'body'):
            for child in node.body: 
                self._extract_methods_data_recursively(child, method_obj, class_name)
        
        # If Else nodes separate the body of the orelse sections.
        if hasattr(node, 'orelse'):
            for orelse in node.orelse:
                if hasattr(orelse, 'body'):
                    for child in orelse.body:
                        self._extract_methods_data_recursively(child, method_obj, class_name)
                else:
                    self._extract_methods_data_recursively(orelse, method_obj, class_name)

    def _extract_return_type(self, returns: astroid.Subscript, class_name: str) -> None:
        """
        Extracts the return type of a method and adds it to the possible coupled 
            classes of the given class, if it is not a built-in type.
        """
        if hasattr(returns, 'slice'):
            # If there is ".slice", the return is of format 'dict[str, Class]'
            self.classes[class_name].possible_coupled_classes.add(
                returns.value.as_string()
            )
            if hasattr(returns.slice, 'elts'):
                for slice in returns.slice.elts:
                    self.classes[class_name].possible_coupled_classes.add(
                        slice.as_string()
                    )
            else:
                self.classes[class_name].possible_coupled_classes.add(
                    returns.slice.as_string()
                )
        else:
            # Simple return
            self.classes[class_name].possible_coupled_classes.add(
                returns.as_string()
            )

                            
    def _extract_inheritance(
        self, base: astroid.FunctionDef, class_name: str
    ) -> None:
        """
        Extract the inheritance information for the given class.
        """
        base_class = base.name
        # Create base_class, if doesnt exist
        self.classes[base_class] = self._get_class(base_class)

        self.classes[class_name].parents.append(self.classes[base_class])
        self.classes[class_name].add_coupled_class(base_class)

    def _extract_classes_data(self, module: astroid.Module) -> None:
        
        """
        Extracts the data from a class node, including methods and attributes,
            and stores it in the classes dictionary.
        Also extracts classes inheritance data.
        """
        
        for node in module.body:
            if isinstance(node, astroid.ClassDef):
                class_name = node.name
                self.classes[class_name] = self._get_class(class_name)
                self.classes[class_name].file = module.path
                self.classes[class_name].lloc = self.count_lloc(node)

                # Extract methods and attributes
                for class_node in node.body:

                    # Method instantiation
                    if isinstance(class_node, astroid.FunctionDef):
                        self._extract_methods(class_node, class_name)

                    # Attribute assign
                    if isinstance(class_node, astroid.Assign):
                        for target in class_node.targets:
                            attr_name = target.name
                            self.classes[class_name].variables.add(attr_name)
                            
                    # Method call or attribute access
                    if isinstance(class_node, (astroid.Expr, astroid.Assign)):
                        self._extract_used_attributes_recursive(
                            class_node.value, self.classes[class_name], class_name
                        )

                # Extract inheritance information
                for base in node.bases:
                    if isinstance(base, astroid.Name):
                        self._extract_inheritance(base, class_name)

    def extract_code_data(self, code: str, path: str = '') -> None:
        """
        Extract the data from the given code string.
        """
        module = astroid.parse(code, path=path)

        self._extract_classes_data(module)

    def process_possible_coupled_classes(self) -> None:
        """
        Process the possible coupled classes for each class in the dictionary.
        """
        all_classes = set(self.classes.keys())
        for class_obj in self.classes.values():
            class_obj.process_possible_coupled_classes(all_classes)


# Test execution
if __name__ == "__main__":
    cp = CodeParser()
    cp.extract_code_data(r"""
                         
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

    """)
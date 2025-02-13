# PyCKTool

**PyCKTool** is an open-source Python library designed to calculate object-oriented and code-level metrics from Python3 source code. It calculates a total of 12 metrics from classes and methods, include all Chidamber & Kemerer metrics.

## Installation

To install PyCKTool, download the source code and run the following command from the project directory:

```bash
pip install .
```

## Usage

Once installed, PyCKTool can be executed from the command line using the following syntax:

```bash
python -m pycktool [path] --format ['csv', 'json'] --output-name OUTPUT_FILE_NAME
```

- path: The directory containing the Python code to be analyzed.
- --format: Specifies the output format (csv or json).
- --output-name: The name of the output file (without extension).

Example

```bash
python -m pycktool ./my_python_project --format csv --output-name metrics_report
```

This will analyze the ./my_python_project directory and save the metrics as a CSV file named metrics_report.csv.

## Metrics

Usually, low values in metrics are expected. High values indicate that the element examined needs attention.

### Class-Level Metrics

1. **Weighted Methods per Class (WMC)**
The sum of the complexities of all methods in a class. Calculated by the sum of LLOCs of methods in the class. 
High values indicate that the class has too many responsibilities, and could be splitted into different classes.
1. **Depth of Inheritance Tree (DIT)**
The length of the longest path from a class to the root class in the inheritance hierarchy. 
High values indicate worst maintainability, since classes with too many superclasses might need knowledge of all the inheritance tree to be altered.
1. **Number of Children (NOC)**
The number of immediate subclasses of a class. 
High values indicate worst maintainability, since changes in the class might impact all of its children.
1. **Coupling Between Classes (CBO)**
The count of distinct classes that a given class is directly coupled to (via imports, attributes, or method calls). Calculated by the sum of Fan In and Fan Out. 
High values indicate that the class is coupled with many classes, so changes in this class might hame many unwanted side effects.
1. **Response for Class (RFC)**
The number of methods that can potentially be executed in response to a message sent to an object of the class. 
High values indicate that the class has too many responsibilities, and could be splitted into different classes.
1. **Lack of Cohesion (LCOM)**
Measures the degree of relatedness between methods and attributes in a class. Low cohesion indicates poor internal organization. Calculated by LCOM4.
LCOM4 builds a graph where all the vertices are methods and attributes, and edges are uses. So, if a method uses an attribute, or calls another method, an edge connects them. Then, LCOM4 counts how many clusters are in the graph. A connected graph has one cluster.
The desired value of the metric is 1. If LCOM calculates as 2 or more, it indicates that the class has more than one responsibility, and should be splitted. If the result is zero, the class has no methods.
1. **Fan In (FIN)**
The number of classes that reference a given class.
High values indicate that the class is coupled with many classes, so changes in this class might hame many unwanted side effects.
1. **Fan Out (FOUT)**
The number of other classes referenced by a given class.
High values indicate that the class is coupled with many classes, so changes in this class might hame many unwanted side effects.
1. **Logical Lines of Code (LLOC)**
The count of actual code lines, excluding comments and blank lines.
High values indicate that the class is too big, could be hard to maintain and possibly could be splitted into different classes.
1. **Number of Attributes (NOA)**
The number of instance variables defined in a class.
High values indicate that the class is too big, could be hard to maintain and possibly could be splitted into different classes.
1. **Number of Methods (NOM)**
The number of methods defined in a class.
High values indicate that the class is too big, could be hard to maintain and possibly could be splitted into different classes.

### Method-Level Metrics

1. **Number of Parameters (NOP)**
The count of parameters accepted by a method.
High values indicate that the method has no specific responsibility, and could possibly be splitter into diffrent methods.
1. **Logical Lines of Code (LLOC)**
High values indicate that the method has no specific responsibility, and could possibly be splitter into diffrent methods.

## Contributing

Contributions to PyCKTool are welcome! If you'd like to contribute, please fork the repository and submit a pull request. For any issues or feature requests, please open an issue in the repository.

## License

PyCKTool is released under the MIT License.

## About

This tool was developed as part of my graduation thesis, "PyCKTool: Ferramenta para Coleta de Métricas de Software Orientado a Objetos em Código Python". The research and development work behind this project provided the foundation for the features introduced in version 1.0.0.
# PyCKTools

**PyCKTools** is an open-source Python library designed to calculate object-oriented and code-level metrics from Python3 source code.  

## Installation

To install PyCKTools, download the source code and run the following command from the project directory:

```bash
pip install .
```

## Usage

Once installed, PyCKTools can be executed from the command line using the following syntax:

```bash
python -m pycktools [path] --format ['csv', 'json'] --output-name OUTPUT_FILE_NAME
```

- path: The directory containing the Python code to be analyzed.
- --format: Specifies the output format (csv or json).
- --output-name: The name of the output file (without extension).

Example

```bash
python -m pycktools ./my_python_project --format csv --output-name metrics_report
```

This will analyze the ./my_python_project directory and save the metrics as a CSV file named metrics_report.csv.

## Metrics

### Class-Level Metrics

1. **Weighted Methods per Class (WMC)**
The sum of the complexities of all methods in a class. Calculated by the sum of LLOCs of methods in the class.
1. **Depth of Inheritance Tree (DIT)**
The length of the longest path from a class to the root class in the inheritance hierarchy.
1. **Number of Children (NOC)**
The number of immediate subclasses of a class.
1. **Coupling Between Classes (CBO)**
The count of distinct classes that a given class is directly coupled to (via imports, attributes, or method calls). Calculated by the sum of Fan In and Fan Out.
1. **Response for Class (RFC)**
The number of methods that can potentially be executed in response to a message sent to an object of the class.
1. **Lack of Cohesion (LCOM)**
Measures the degree of relatedness between methods in a class. Low cohesion indicates poor organization. Calculated as the number of attribute of the class, divided by the total number of methods in the class.
1. **Fan In (FIN)**
The number of classes that reference a given class.
1. **Fan Out (FOUT)**
The number of other classes referenced by a given class.
1. **Logical Lines of Code (LLOC)**
The count of actual code lines, excluding comments and blank lines.
1. **Number of Attributes (NOA)**
The number of instance variables defined in a class.
1. **Number of Methods (NOM)**
The number of methods defined in a class.

### Method-Level Metrics

1. **Number of Parameters (NOP)**
The count of parameters accepted by a method.
1. **Logical Lines of Code (LLOC)**
The number of code lines inside a method, excluding comments and blank lines.

## Contributing

Contributions to PyCKTools are welcome! If you'd like to contribute, please fork the repository and submit a pull request. For any issues or feature requests, please open an issue in the repository.

## License

PyCKTools is released under the MIT License.

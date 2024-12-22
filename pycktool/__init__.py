
import argparse

from pycktool.pycktool_run import PyCKTool

'''
This module contains the main() function, which is the entry point for the
command line interface.
'''

__version__ = '1.0.0'

def main():
    '''The entry point for Setuptools.'''

    parser = argparse.ArgumentParser(description="Execute PyCKTool from the console.")
    parser.add_argument(
        "path", type=str, help="Path of the analyzed code.", default='.', nargs='?'
    )
    parser.add_argument(
        "--format", type=str, help="Format of the output file.", default='csv',
        choices=['csv', 'json']
    )
    # TODO: Use output name
    parser.add_argument(
        "--output-prefix", type=str, help="Prefix of the output result files.",
        dest='prefix', default=''
    )
    args = parser.parse_args()

    try:
        PyCKTool.run(args.path, args.format, args.prefix)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()

import argparse

from pycktools.pycktools_run import run

'''
This module contains the main() function, which is the entry point for the
command line interface.
'''

__version__ = '1.0.0'

def main():
    '''The entry point for Setuptools.'''

    parser = argparse.ArgumentParser(description="Execute MyLibrary from the console.")
    parser.add_argument(
        "path", type=str, help="Path of the analyzed code.", default='.', nargs='?'
    )
    parser.add_argument(
        "--format", type=str, help="Format of the output file.", default='csv',
        choices=['csv', 'json']
    )
    # TODO: Use output name
    parser.add_argument(
        "--output-name", type=str, help="Name of the output file."
    )
    args = parser.parse_args()

    try:
        run(args.path, args.format)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
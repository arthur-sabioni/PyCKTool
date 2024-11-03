'''This module contains the main() function, which is the entry point for the
command line interface.'''
__version__ = '1.0.0'

def main():
    '''The entry point for Setuptools.'''
    import sys
    from pycktools.pycktools import run

    print(sys.argv)
    if not sys.argv[1]:
        print('No path specified.')
        exit(1)
    if not sys.argv[2]:
        sys.argv.append('csv')
    try:
        run(sys.argv[1], sys.argv[2])
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
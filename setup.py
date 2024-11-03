from setuptools import setup, find_packages
import os

with open(os.path.join('README.md'), 'r') as f:
    long_description = f.read()
    
with open(os.path.join('pycktools', 'requirements.txt')) as f:
    requirements = f.readlines()

setup(
    name='pycktools',
    version=1.0,
    author='Arthur Lopes Sabioni',
    author_email='arthur.lsabioni@gmail.com',
    license='MIT',
    long_description=long_description,
    description='Chidamber and Kemerer metrics for Python',
    platforms='any',
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "pycktools=pycktools.main:main",
        ],
    },
    install_requires=requirements,
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Quality Assurance',
        'Topic :: Utilities',
    ]
)

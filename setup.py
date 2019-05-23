"""
A setuptools based setup module.

See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""
from setuptools import setup, find_packages
from os import path

from io import open
here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='log_reader', 

    version='0.1.0',

    description='A simple example that reads a json file and does some analysis',
    long_description=long_description,  
    long_description_content_type='text/x-rst',  # long description is restructured text format

    author='Shannon Jaeger',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Software Development :: Code Sample',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
    ],

    packages=find_packages(exclude=['docs', 'tests']), 
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, <4',

    install_requires=['pandas'], 
    extras_require={  
        'test': ['nosetests', 'pathlib'],
    },

    entry_points={  # Optional
        'console_scripts': [
            'json_log=run:main',
        ],
    },

)


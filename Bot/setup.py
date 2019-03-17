from setuptools import setup, find_packages
from os.path import join, dirname
import core

setup(
    name='server-mo',
    version=core.__version__,
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.txt')).read(),
    install_requires=[
        'Flask==1.0.2'
    ]
)

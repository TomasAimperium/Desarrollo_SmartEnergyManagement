from distutils.core import setup, Extension
from Cython.Build import cythonize
import numpy
import random

setup(
    ext_modules=cythonize(['cost_function_.pyx']),
    include_dirs=[numpy.get_include()]
)   



# python setup.py build_ext --inplace
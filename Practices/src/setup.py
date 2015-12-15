from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutuils import build_ext

setup(cmdclass={'build_ext': build_ext}, ext_modules = [Extension("generator", ["cython_generator.pyx"])]
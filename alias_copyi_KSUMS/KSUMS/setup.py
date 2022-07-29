import os
import numpy
from Cython.Build import cythonize

def configuration(parent_package='', top_path=None):
    from numpy.distutils.misc_util import Configuration

    cpp_version = "c++17"
    if os.name == "nt":
        ext_comp_args = ['/']
        ext_link_args = []

        library_dirs = []
        libraries = []
    else:
        ext_comp_args = ['-fopenmp', f'-std={cpp_version}']
        ext_link_args = ['-fopenmp', f'-std={cpp_version}']
        library_dirs = []
        libraries = ["m"]

    fpath, fname = os.path.split(os.path.abspath(__file__))
    cpath = os.path.join(fpath, "../Public/CppFuns/")

    config = Configuration('KSUMS', parent_package, top_path)

    config.add_extension('KSUMS_',
                         sources=['KSUMS_.pyx'],
                         include_dirs=[numpy.get_include(), cpath],
                         language="c++",
                         libraries=libraries)

    config.ext_modules = cythonize(config.ext_modules, compiler_directives={'language_level': 3})

    return config


if __name__ == '__main__':
    from numpy.distutils.core import setup
    setup(**configuration(top_path='').todict())

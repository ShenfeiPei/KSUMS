import os
import numpy
from Cython.Build import cythonize
from KSUMS_pack.Public import cg


def configuration(parent_package='', top_path=None):
    from numpy.distutils.misc_util import Configuration

    config = Configuration('KSUMS', parent_package, top_path)

    config.add_extension('KSUMS_',
                         sources=['KSUMS_.pyx'],
                         include_dirs=[numpy.get_include(), cg.cppfuns_path],
                         language="c++",
                         libraries=cg.libraries)

    config.ext_modules = cythonize(config.ext_modules, compiler_directives={'language_level': 3})

    return config


if __name__ == '__main__':
    from numpy.distutils.core import setup
    setup(**configuration(top_path='').todict())

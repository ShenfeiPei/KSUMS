import os
import numpy
from Cython.Build import cythonize
from Public import cg


def configuration(parent_package='', top_path=None):
    from numpy.distutils.misc_util import Configuration

    config = Configuration('CppFuns', parent_package, top_path)
    config.add_extension('Graph_',
                         sources=['Graph_.pyx'],
                         include_dirs = [numpy.get_include()],
                         language="c++",

                         extra_compile_args=cg.ext_comp_args,
                         extra_link_args=cg.ext_link_args,

                         library_dirs=cg.library_dirs,
                         libraries=cg.libraries,

                         define_macros=cg.define_macros,
                         )

    config.add_extension('Keep_order_',
                         sources=['Keep_order_.pyx'],
                         include_dirs=[numpy.get_include()],
                         language="c++",

                         extra_compile_args=cg.ext_comp_args,
                         extra_link_args=cg.ext_link_args,

                         library_dirs=cg.library_dirs,
                         libraries=cg.library_dirs,

                         define_macros=cg.define_macros,
                         )

    config.ext_modules = cythonize(config.ext_modules, compiler_directives={'language_level': 3})

    return config


if __name__ == '__main__':
    from numpy.distutils.core import setup
    setup(**configuration(top_path='').todict())

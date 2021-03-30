import setuptools  # noqa
import os
from numpy.distutils.core import setup
from distutils.command.sdist import sdist
from numpy.distutils.misc_util import Configuration


def configuration(parent_package='', top_path=None):
    if os.path.exists('MANIFEST'):
        os.remove('MANIFEST')

    config = Configuration(None, parent_package, top_path)

    config.set_options(ignore_setup_xxx_py=True,
                       assume_default_configuration=True,
                       delegate_options_to_subpackages=True,
                       quiet=True)
    config.add_subpackage('KSUMS2')
    return config


setup(name="KSUMS2",
      version="0.0.1",
      author="Shenfei Pei",
      author_email="shenfeipei@gmail.com",
      description="A Python module for machine learning",
      url="https://github.com/ShenfeiPei/KSUMS",
      install_requires=['numpy>=1.16.5', 'scipy>=1.3.1', 'pandas>=0.25.1', 'scikit-learn>=0.21.3'],
      # install_requires=min_deps.tag_to_packages['install'],
      classifiers=['Intended Audience :: Science/Research',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: MIT License',
                   'Programming Language :: C',
                   'Programming Language :: Python',
                   'Topic :: Software Development',
                   'Topic :: Scientific/Engineering',
                   'Operating System :: Microsoft :: Windows',
                   'Programming Language :: Python :: 3.8',
                   ('Programming Language :: Python :: '
                    'Implementation :: CPython')
                   ],
      cmdclass={'sdist': sdist},
      python_requires=">=3.8",
      configuration=configuration)

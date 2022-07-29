import setuptools  # noqa
import os
import shutil
from numpy.distutils.core import setup
from distutils.command.sdist import sdist
from numpy.distutils.misc_util import Configuration
from distutils.command.clean import clean as Clean

module_name = "alias_copyi_KSUMS"

class CleanCommand(Clean):
    description = "Remove build artifacts from the source tree"

    def run(self):
        Clean.run(self)
        # Remove c files if we are not within a sdist package
        cwd = os.path.abspath(os.path.dirname(__file__))
        remove_c_files = not os.path.exists(os.path.join(cwd, 'PKG-INFO'))
        if remove_c_files:
            print('Will remove generated .c files')
        if os.path.exists('build'):
            shutil.rmtree('build')
        
        egg_info_path = f"{module_name}.egg-info"
        if os.path.exists(egg_info_path):
            shutil.rmtree(egg_info_path)

        for dirpath, dirnames, filenames in os.walk(module_name):
            for filename in filenames:
                if any(filename.endswith(suffix) for suffix in
                       (".so", ".pyd", ".dll", ".pyc")):
                    os.unlink(os.path.join(dirpath, filename))
                    continue
                extension = os.path.splitext(filename)[1]
                if remove_c_files and extension in ['.c', '.cpp']:
                    pyx_file = str.replace(filename, extension, '.pyx')
                    if os.path.exists(os.path.join(dirpath, pyx_file)):
                        os.unlink(os.path.join(dirpath, filename))
            for dirname in dirnames:
                if dirname == '__pycache__':
                    shutil.rmtree(os.path.join(dirpath, dirname))


def configuration(parent_package='', top_path=None):
    if os.path.exists('MANIFEST'):
        os.remove('MANIFEST')

    config = Configuration(None, parent_package, top_path)

    config.set_options(ignore_setup_xxx_py=True,
                       assume_default_configuration=True,
                       delegate_options_to_subpackages=True,
                       quiet=True)
    config.add_subpackage(module_name)
    return config


setup(name=module_name,
      version="0.0.3",
      author="Shenfei Pei",
      author_email="shenfeipei@gmail.com",
      description="A python implementation of 'KSUMS', NeurIPS, 2020",
      url="https://github.com/ShenfeiPei/KSUMS",
      install_requires=['numpy>=1.20.3', 'scipy>=1.5.3', 'pandas>=1.2.3', 'scikit-learn>=0.22.2'],
      classifiers=['Intended Audience :: Science/Research',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: MIT License',
                   'Programming Language :: C++',
                   'Programming Language :: Python',
                   'Topic :: Software Development',
                   'Topic :: Scientific/Engineering',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python :: 3.8',
                   ('Programming Language :: Python :: '
                    'Implementation :: CPython')
                   ],
      cmdclass={'clean': CleanCommand, 'sdist': sdist},
      python_requires=">=3.8",
      configuration=configuration)

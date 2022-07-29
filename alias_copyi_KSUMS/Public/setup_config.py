import os

public_path = os.path.abspath(__file__)
public_path = os.path.dirname(public_path)
cppfuns_path = public_path + os.path.sep + "CppFuns"
eigen339_path = public_path + os.path.sep + "Eigen339"
mpir_path = public_path + os.path.sep + "MPIR"


cpp_version = "c++11"

if os.name == "nt":
    ext_comp_args = ['/openmp']
    ext_link_args = ['/openmp']

    library_dirs = []
    libraries = []
else:
    ext_comp_args = ['-fopenmp']
    ext_link_args = ['-fopenmp']

    library_dirs = []
    libraries = ["m"]

define_macros=[("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")]
                         

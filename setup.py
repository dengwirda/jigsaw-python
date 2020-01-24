
import io, os
import subprocess
import shutil

from setuptools import setup, find_packages, Command

NAME = "jigsawpy"
DESCRIPTION = \
    "Python interface for the JIGSAW meshing library."
AUTHOR = "Darren Engwirda"
AUTHOR_EMAIL = "darren.engwirda@columbia.edu"
URL = "https://github.com/dengwirda/"
VERSION = "0.1.0"
REQUIRES_PYTHON = ">=3.6.0"
KEYWORDS = "Mesh-generation Delaunay Voronoi"

REQUIRED = [
    "numpy", "pathlib"
]

CLASSIFY = [
    "Development Status :: 3 - Alpha",
    "Operating System :: OS Independent",
    "Intended Audience :: Science/Research",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Topic :: Scientific/Engineering",
    "Topic :: Scientific/Engineering :: Mathematics",
    "Topic :: Scientific/Engineering :: Physics",
    "Topic :: Scientific/Engineering :: Visualization"
]

here = os.path.abspath(os.path.dirname(__file__))

try:
    with io.open(os.path.join( \
        here,"README.md"),encoding="utf-8") as f:
        LONG_DESCRIPTION = "\n"+f.read()

except FileNotFoundError:
    LONG_DESCRIPTION = DESCRIPTION


class build_external(Command):

    description = "build external JIGSAW dependencies"

    user_options = []

    def initialize_options(self): pass

    def finalize_options(self): pass

    def run(self):
        """
        The actual cmake-based build steps for JIGSAW
        
        """
        if (self.dry_run): return

        cwd_pointer = os.getcwd()

        try:
            self.announce("cmake config.",level=3)

            source_path = \
            os.path.join(here,"external","jigsaw")

            builds_path = \
            os.path.join(source_path,"tmp")

            os.makedirs(builds_path,exist_ok=True)

            exesrc_path = \
            os.path.join(source_path,"bin")

            libsrc_path = \
            os.path.join(source_path,"lib") 

            exedst_path = \
            os.path.join(here,"jigsawpy","_bin")

            libdst_path = \
            os.path.join(here,"jigsawpy","_lib")

            shutil.rmtree(
                exedst_path,ignore_errors=True)
            shutil.rmtree(
                libdst_path,ignore_errors=True)

            os.chdir(builds_path)

            config_call = \
        ["cmake", "..","-DCMAKE_BUILD_TYPE=Release"]

            subprocess.run(config_call,check=True)

            self.announce("cmake complie",level=3)

            compilecall = \
        ["cmake","--build",".","--config","Release",
                               "--target","install"]

            subprocess.run(compilecall,check=True)

            self.announce("cmake cleanup",level=3)

            shutil.copytree(exesrc_path,exedst_path)
            shutil.copytree(libsrc_path,libdst_path)

        finally:
            os.chdir(cwd_pointer)

            shutil.rmtree (builds_path)


setup(
    name = NAME,
    version = VERSION,
    description = DESCRIPTION,
    long_description = LONG_DESCRIPTION,
    long_description_content_type = "text/markdown",
    license = "custom",    
    author = AUTHOR,
    author_email = AUTHOR_EMAIL,
    python_requires = REQUIRES_PYTHON,
    keywords = KEYWORDS,    
    url = URL,
    packages = find_packages (),
    cmdclass = {
        "build_external" : build_external
        },
    package_data = {"jigsawpy": ["_bin/*", "_lib/*"]
        },
    install_requires = REQUIRED,
    classifiers = CLASSIFY
)




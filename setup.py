
import io
import os
from setuptools import setup, find_packages, Command

#-- old setup.py workflow for backwards compatibility
#-- python setup.py build_external
#-- python setup.py install 

NAME = "jigsawpy"
DESCRIPTION = \
    "Python interface for the JIGSAW meshing library."
AUTHOR = "Darren Engwirda"
AUTHOR_EMAIL = "d.engwirda@gmail.com"
URL = "https://github.com/dengwirda/"
VERSION = "1.1.0"
REQUIRES_PYTHON = ">=3.6.0"
KEYWORDS = "Mesh-generation Delaunay Voronoi"

REQUIRED = [
    "numpy", "scipy"
]

CLASSIFY = [
    "Development Status :: 5 - Production/Stable",
    "Operating System :: OS Independent",
    "Intended Audience :: Science/Research",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: C++",
    "Topic :: Scientific/Engineering",
    "Topic :: Scientific/Engineering :: Mathematics",
    "Topic :: Scientific/Engineering :: Physics",
    "Topic :: Scientific/Engineering :: Visualization"
]

HERE = os.path.abspath(os.path.dirname(__file__))

try:
    with io.open(os.path.join(
            HERE, "README.md"), encoding="utf-8") as f:
        LONG_DESCRIPTION = "\n" + f.read()

except FileNotFoundError:
    LONG_DESCRIPTION = DESCRIPTION


class build_external(Command):

    description = "build external JIGSAW dependencies"

    user_options = []

    def initialize_options(self): pass

    def finalize_options(self): pass

    def run(self):
        if (self.dry_run): return
        import build; build.build_external()


setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    python_requires=REQUIRES_PYTHON,
    keywords=KEYWORDS,
    url=URL,
    packages=find_packages(exclude=["tests",]),
    cmdclass={"build_external": build_external},
    package_data={"jigsawpy": ["_bin/*", "_lib/*"]},
    install_requires=REQUIRED,
    classifiers=CLASSIFY
)


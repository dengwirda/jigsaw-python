## `JIGSAW: An unstructured mesh generator`

<p align="middle">
  <img src = "../master/external/jigsaw/img/bunny-TRIA3-1.png" width="20%" hspace="0.25%">
  <img src = "../master/external/jigsaw/img/bunny-TRIA3-2.png" width="20%" hspace="0.25%">
  <img src = "../master/external/jigsaw/img/bunny-TRIA3-3.png" width="20%" hspace="0.25%">
  <img src = "../master/external/jigsaw/img/bunny-TRIA4-3.png" width="20%" hspace="0.25%">
</p>

`JIGSAW` is an unstructured mesh generator and tessellation library; designed to generate high-quality triangulations and polyhedral decompositions of general planar, surface and volumetric domains. `JIGSAW` includes refinement-based algorithms for the construction of new meshes, optimisation-driven techniques for the improvement of existing grids, as well as routines to assemble (restricted) Delaunay tessellations, Voronoi complexes and Power diagrams.

This package provides a <a href="http://www.python.org">`Python`</a> based scripting interface to the underlying `JIGSAW` mesh generator, including a range of additional facilities for file I/O, mesh visualisation and post-processing operations.

`JIGSAW` has been compiled and tested on various `64-bit` `Linux` , `Windows` and `Mac` based platforms. 

### `Quickstart`

    Ensure you have a c++ compiler and the cmake utility installed.
    Clone/download + unpack this repository.
    python3 setup.py build_external
    python3 setup.py install
    python3 example.py --IDnumber=0
    
Note: installation of `JIGSAW` requires a `c++` compiler and the `cmake` utility. `JIGSAW` may also be installed as a `conda` package. See <a href="https://github.com/dengwirda/jigsaw">here</a> for details.
    
### `Function Listing`

See `jigsawpy` for a description of the various functions available.

    setup.py    - compile and install JIGSAW's c++ backend using cmake.
    example.py  - a list of demo programs. 
    
    jigsaw.py   - cmd-line interface to JIGSAW's backend
    libsaw.py   - api-lib. interface to JIGSAW's backend
    
    loadmsh.py  - load *.msh files.
    savemsh.py  - save *.msh files.
    loadjig.py  - load *.jig files.
    savejig.py  - save *.jig files.

    project.py  - apply cartographic projection operators to mesh obj.

    bisect.py   - refine a mesh obj. via bisection.
    extrude.py  - create a mesh obj. via extrusion.

### `Example Problems`

The following set of example problems are available in `example.py`:

    example: 0; # simple 2-dim. examples to get started
    example: 1; # simple 3-dim. examples to get started
    example: 2; # frontal-delaunay methods in the plane
    example: 3; # frontal-delaunay methods for surfaces
    example: 4; # frontal-delaunay methods for volumes
    example: 5; # user-defined mesh-spacing constraints
    example: 6; # dealing with sharp-features in piecewise smooth domains
    example: 7; # dealing with sharp-features in piecewise smooth domains
    example: 8; # (re)mesh marching-cubes style outputs
    example: 9; # creating prismatic volumes via extrusion

Run `python3 example.py --IDnumber=N` to call the `N-th` example. `*.vtk` output is saved to `../cache` and can be visualised with, for example, <a href=https://www.paraview.org/>Paraview</a>.

### `License`

This program may be freely redistributed under the condition that the copyright notices (including this entire header) are not removed, and no compensation is received through use of the software.  Private, research, and institutional use is free.  You may distribute modified versions of this code `UNDER THE CONDITION THAT THIS CODE AND ANY MODIFICATIONS MADE TO IT IN THE SAME FILE REMAIN UNDER COPYRIGHT OF THE ORIGINAL AUTHOR, BOTH SOURCE AND OBJECT CODE ARE MADE FREELY AVAILABLE WITHOUT CHARGE, AND CLEAR NOTICE IS GIVEN OF THE MODIFICATIONS`. Distribution of this code as part of a commercial system is permissible `ONLY BY DIRECT ARRANGEMENT WITH THE AUTHOR`. (If you are not directly supplying this code to a customer, and you are instead telling them how they can obtain it for free, then you are not required to make any arrangement with me.) 

`DISCLAIMER`:  Neither I nor: Columbia University, the Massachusetts Institute of Technology, the University of Sydney, nor the National Aeronautics and Space Administration warrant this code in any way whatsoever.  This code is provided "as-is" to be used at your own risk.

### `References`

There are a number of publications that describe the algorithms used in `JIGSAW` in detail. If you make use of `JIGSAW` in your work, please consider including a reference to the following:

`[1]` - Darren Engwirda: Generalised primal-dual grids for unstructured co-volume schemes, J. Comp. Phys., 375, pp. 155-176, https://doi.org/10.1016/j.jcp.2018.07.025, 2018.

`[2]` - Darren Engwirda, Conforming Restricted Delaunay Mesh Generation for Piecewise Smooth Complexes, Procedia Engineering, 163, pp. 84-96, https://doi.org/10.1016/j.proeng.2016.11.024, 2016.

`[3]` - Darren Engwirda, Voronoi-based Point-placement for Three-dimensional Delaunay-refinement, Procedia Engineering, 124, pp. 330-342, http://dx.doi.org/10.1016/j.proeng.2015.10.143, 2015.

`[4]` - Darren Engwirda, David Ivers, Off-centre Steiner points for Delaunay-refinement on curved surfaces, Computer-Aided Design, 72, pp. 157-171, http://dx.doi.org/10.1016/j.cad.2015.10.007, 2016.

`[5]` - Darren Engwirda, Locally-optimal Delaunay-refinement and optimisation-based mesh generation, Ph.D. Thesis, School of Mathematics and Statistics, The University of Sydney, http://hdl.handle.net/2123/13148, 2014.


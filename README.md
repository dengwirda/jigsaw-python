## `JIGSAW(GEO): Mesh generation for geoscientific modelling`

<p align="center">
  <img src = "image/voro.jpg">
</p>

`JIGSAW(GEO)` is a set of algorithms designed to generate unstructured grids for geoscientific modelling. Applications include: large-scale atmospheric simulation and numerical weather prediction, global and coastal ocean-modelling, and ice-sheet dynamics. 

`JIGSAW(GEO)` can be used to produce high-quality 'generalised' Delaunay / Voronoi tessellations for unstructured finite-volume / element type models. Grids can be generated in local two-dimensional domains, and over general spheroidal surfaces. Mesh resolution can be adapted to follow complex user-defined metrics, including: topographic contours, discrete solution profiles or coastal features. These features enable the generation of complex, multi-resolution climate process models, with simulation fidelity enhanced in regions of interest.

`JIGSAW(GEO)` is a stand-alone mesh generator written in `c++`, based on <a href="https://github.com/dengwirda/jigsaw">`JIGSAW`</a> - a general purpose meshing package. This toolbox provides a <a href="https://www.python.org/">`Python`</a> based interface, including `file I/O`, `mesh visualisation` and `post-processing` facilities. The underlying `JIGSAW` library is a collection of unstructured triangle- and tetrahedron-based meshing algorithms, designed to produce high quality Delaunay-based grids for computational simulation. `JIGSAW` includes both Delaunay-refinement based algorithms for the construction of new meshes, as well as optimisation driven methods for the improvement of existing grids. 

`JIGSAW(GEO)` is typically able to produce the very high-quality staggered unstructured grids required by contemporary unstructued general circulation models (i.e. <a href="https://github.com/MPAS-Dev/MPAS-Release">`MPAS`</a>, <a href="https://research.csiro.au/cem/software/ems/hydro/unstructured-compas/">`COMPAS`</a>, <a href="http://fesom.de/">`FESOM`</a>, <a href="https://www.mpimet.mpg.de/en/science/models/icon-esm/">`ICON`</a>, etc), generating highly optimised, multi-resolution meshes that are `locally-orthogonal`, `mutually-centroidal` and `self-centred`.

`JIGSAW(GEO)` has been compiled and tested on various `64-bit` `Linux` , `Windows` and `Mac` based platforms. 

## `Getting Started`

The first step is to compile and configure the underlying `JIGSAW` `c++` library. `JIGSAW` can either be built directly from src, or installed using the <a href="https://anaconda.org/conda-forge/jigsaw">`conda`</a> package manager. More details can be found <a href="https://github.com/dengwirda/jigsaw">here</a>. 


## `Example Problems`

After downloading and building the code, navigate to the root `JIGSAW(GEO)` directory to run the set of examples contained in `example.py`:
````
example(1); % simple 2-dim. examples to get stated.
example(2); % a multi-resolution grid for the Australian region.
example(3); % a multi-part grid of the (contiguous) USA.
example(4); % a uniform-resolution spheroidal grid.
example(5); % a spheroidal grid with a regional "patch".
example(6); % a spheroidal grid with complex grid-spacing constraints.
````

## `License`

This program may be freely redistributed under the condition that the copyright notices (including this entire header) are not removed, and no compensation is received through use of the software.  Private, research, and institutional use is free.  You may distribute modified versions of this code `UNDER THE CONDITION THAT THIS CODE AND ANY MODIFICATIONS MADE TO IT IN THE SAME FILE REMAIN UNDER COPYRIGHT OF THE ORIGINAL AUTHOR, BOTH SOURCE AND OBJECT CODE ARE MADE FREELY AVAILABLE WITHOUT CHARGE, AND CLEAR NOTICE IS GIVEN OF THE MODIFICATIONS`. Distribution of this code as part of a commercial system is permissible `ONLY BY DIRECT ARRANGEMENT WITH THE AUTHOR`. (If you are not directly supplying this code to a customer, and you are instead telling them how they can obtain it for free, then you are not required to make any arrangement with me.) 

`DISCLAIMER`:  Neither I nor: Columbia University, the Massachusetts Institute of Technology, the University of Sydney, nor the National Aeronautics and Space Administration warrant this code in any way whatsoever.  This code is provided "as-is" to be used at your own risk.

## `References`

There are a number of publications that describe the algorithms used in `JIGSAW(GEO)` in detail. Additional information and references regarding the formulation of the underlying `JIGSAW` mesh-generator can also be found <a href="https://github.com/dengwirda/jigsaw">here</a>. If you make use of `JIGSAW` in your work, please consider including a reference to the following: 

`[1]` - Darren Engwirda: Generalised primal-dual grids for unstructured co-volume schemes, J. Comp. Phys., 375, pp. 155-176, https://doi.org/10.1016/j.jcp.2018.07.025, 2018.

`[2]` - Darren Engwirda: JIGSAW-GEO (1.0): locally orthogonal staggered unstructured grid generation for general circulation modelling on the sphere, Geosci. Model Dev., 10, pp. 2117-2140, https://doi.org/10.5194/gmd-10-2117-2017, 2017.

`[3]` - Darren Engwirda, David Ivers, Off-centre Steiner points for Delaunay-refinement on curved surfaces, Computer-Aided Design, 72, pp. 157-171, http://dx.doi.org/10.1016/j.cad.2015.10.007, 2016.

`[4]` - Darren Engwirda: Multi-resolution unstructured grid-generation for geophysical applications on the sphere, Research note, Proceedings of the 24th International Meshing Roundtable, https://arxiv.org/abs/1512.00307, 2015.

`[5]` - Darren Engwirda, Locally-optimal Delaunay-refinement and optimisation-based mesh generation, Ph.D. Thesis, School of Mathematics and Statistics, The University of Sydney, http://hdl.handle.net/2123/13148, 2014.



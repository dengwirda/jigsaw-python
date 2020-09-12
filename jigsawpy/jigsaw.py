
import subprocess
import os
import inspect
import shutil
import copy
import math
import numpy as np

from pathlib import Path

from jigsawpy.tools.scorecard import trideg2, trideg3, \
    triscr2, triscr3
from jigsawpy.tools.mathutils import S2toR3

from jigsawpy.bisect import bisect

from jigsawpy.jig_t import jigsaw_jig_t
from jigsawpy.msh_t import jigsaw_msh_t

from jigsawpy.loadmsh import loadmsh
from jigsawpy.savemsh import savemsh
from jigsawpy.savejig import savejig


def jigsaw(opts, mesh=None):
    """
    JIGSAW cmd-line interface to JIGSAW.

    JIGSAW(OPTS, MESH=None)

    Call the JIGSAW mesh generator using the config. options
    specified in the OPTS structure.

    OPTS is a user-defined set of meshing options. See JIG_t
    for details.

    """
    jexename = Path()

    if (not isinstance(opts, jigsaw_jig_t)):
        raise Exception("Incorrect type: OPTS.")

    if (mesh is not None and not
            isinstance(mesh, jigsaw_msh_t)):
        raise Exception("Incorrect type: MESH.")

    savejig(opts.jcfg_file, opts)

    if (jexename == Path()):
#---------------------------- set-up path for "local" binary

    #   stackoverflow.com/questions/2632199/
    #       how-do-i-get-the-
    #       path-of-the-current-executed-file-in-python
        filename = \
            inspect.getsourcefile(lambda:0)

        filepath = \
            Path(filename).resolve().parent

        if   (os.name == "nt"):
            jexename = filepath / "_bin" / "jigsaw.exe"

        elif (os.name == "posix"):
            jexename = filepath / "_bin" / "jigsaw"

        if (not jexename.is_file()):
            jexename = Path()

    if (jexename == Path()):
#---------------------------- search machine path for binary
        jexescan = shutil.which("jigsaw")

        if (jexescan is not None):
            jexename = Path(jexescan)

    if (jexename != Path()):
#---------------------------- call JIGSAW and capture output
        subprocess.run([
            str(jexename), opts.jcfg_file], check=True)

        if (mesh is not None):
            loadmsh(opts.mesh_file, mesh)

    else:

        raise Exception("JIGSAW executable not found!")

    return


def tripod(opts, tria=None):
    """
    TRIPOD cmd-line interface to TRIPOD.

    TRIPOD(OPTS, TRIA=None)

    Call the TRIPOD tessellation util. using the config. opt
    specified in the OPTS structure.

    OPTS is a user-defined set of meshing options. See JIG_t
    for details.

    """
    jexename = Path()

    if (not isinstance(opts, jigsaw_jig_t)):
        raise Exception("Incorrect type: OPTS.")

    if (tria is not None and not
            isinstance(tria, jigsaw_msh_t)):
        raise Exception("Incorrect type: TRIA.")

    savejig(opts.jcfg_file, opts)

    if (jexename == Path()):
#---------------------------- set-up path for "local" binary

    #   stackoverflow.com/questions/2632199/
    #       how-do-i-get-the-
    #       path-of-the-current-executed-file-in-python
        filename = \
            inspect.getsourcefile(lambda:0)

        filepath = \
            Path(filename).resolve().parent

        if   (os.name == "nt"):
            jexename = filepath / "_bin" / "tripod.exe"

        elif (os.name == "posix"):
            jexename = filepath / "_bin" / "tripod"

        if (not jexename.is_file()):
            jexename = Path()

    if (jexename == Path()):
#---------------------------- search machine path for binary
        jexescan = shutil.which("tripod")

        if (jexescan is not None):
            jexename = Path(jexescan)

    if (jexename != Path()):
#---------------------------- call JIGSAW and capture output
        subprocess.run([
            str(jexename), opts.jcfg_file], check=True)

        if (tria is not None):
            loadmsh(opts.mesh_file, tria)

    else:

        raise Exception("TRIPOD executable not found!")

    return


def marche(opts, ffun=None):
    """
    MARCHE cmd-line interface to MARCHE.

    MARCHE(OPTS, FFUN=None)

    Call the "fast-marching" solver MARCHE using the config.
    options specified in the OPTS structure. MARCHE solves
    the Eikonal equations

    MAX(||dh/dx||, g) = g,

    where g = g(x) is a gradient threshold applied to h. See
    the SAVEMSH/LOADMSH functions for a description of the
    HFUN output structure.

    OPTS is a user-defined set of meshing options. See JIG_t
    for details.

    """
    jexename = Path()

    if (not isinstance(opts, jigsaw_jig_t)):
        raise Exception("Incorrect type: OPTS.")

    if (ffun is not None and not
            isinstance(ffun, jigsaw_msh_t)):
        raise Exception("Incorrect type: FFUN.")

    savejig(opts.jcfg_file, opts)

    if (jexename == Path()):
#---------------------------- set-up path for "local" binary

    #   stackoverflow.com/questions/2632199/
    #       how-do-i-get-the-
    #       path-of-the-current-executed-file-in-python
        filename = \
            inspect.getsourcefile(lambda:0)

        filepath = \
            Path(filename).resolve().parent

        if   (os.name == "nt"):
            jexename = filepath / "_bin" / "marche.exe"

        elif (os.name == "posix"):
            jexename = filepath / "_bin" / "marche"

        if (not jexename.is_file()):
            jexename = Path()

    if (jexename == Path()):
#---------------------------- search machine path for binary
        jexescan = shutil.which("marche")

        if (jexescan is not None):
            jexename = Path(jexescan)

    if (jexename != Path()):
#---------------------------- call JIGSAW and capture output
        subprocess.run([
            str(jexename), opts.jcfg_file], check=True)

        if (ffun is not None):
            loadmsh(opts.hfun_file, ffun)

    else:

        raise Exception("MARCHE executable not found!")

    return


def metric(mesh):
    """
    METRIC assemble combined "cost" metric for a given mesh.

    """

    cost = np.empty((+0), dtype=mesh.REALS_t)

    if (mesh.tria3 is not None and \
            mesh.tria3.size > +0):
#--------------------------------------- append TRIA3 scores
        COST = triscr2(
            mesh.point["coord"],
            mesh.tria3["index"]
        )

        cost = np.append(cost, COST)

    if (mesh.tria4 is not None and \
            mesh.tria4.size > +0):
#--------------------------------------- append TRIA4 scores
        COST = triscr3(
            mesh.point["coord"],
            mesh.tria4["index"]
        )

        cost = np.append(cost, COST)

    if (cost.size == 0): return +0.0
    
    norm = np.sum((1.0 / cost) ** 3)

    return np.cbrt(cost.size / norm)


def jitter(opts, imax, ibad, mesh=None):
    """
    JITTER call JIGSAW iteratively; try to improve topology.

    """

    if (not isinstance(opts, jigsaw_jig_t)):
        raise Exception("Incorrect type: OPTS.")

    if (mesh is not None and not
            isinstance(mesh, jigsaw_msh_t)):
        raise Exception("Incorrect type: MESH.")

    if (mesh is None): mesh = jigsaw_msh_t()

#--------- call JIGSAW iteratively; try to improve topology.
    OPTS = copy.deepcopy(opts)

    best = metric(mesh); next = mesh; done = False

    for iter in range(imax):

        if (next.point is not None and
                next.point.size != +0):

            nvrt = next.point.size

            keep = np.full(
                (nvrt), True, dtype=bool)

    #------------------------------ setup initial conditions
            path = Path(opts.mesh_file).parent
            name = Path(opts.mesh_file).stem
            fext = Path(opts.mesh_file).suffix

            name = str(name)
            fext = str(fext)
            name = name + "-INIT" + fext

            OPTS.init_file = str(path / name)

            if (next.tria3 is not None and
                    next.tria3.size != +0):

    #------------------------------ mark any irregular nodes
                vdeg = trideg2(
                    next.point["coord"],
                    next.tria3["index"])

                ierr = np.abs(vdeg - 6)  # err in topo. deg.

                ierr[vdeg > 6] = ierr[vdeg > 6] * 2

                ierr = ierr[next.tria3["index"]]

                M = np.sum(ierr, axis=1) >= ibad

                keep[next.tria3["index"][M, :]] = False

            if (next.edge2 is not None and
                    next.edge2.size != +0):

                keep[next.edge2["index"][:, :]] = True

    #------------------------------ don't delete everything!
            if (np.count_nonzero(keep) <= +8):

                keep = np.full(
                    (nvrt), True, dtype=bool)

            done = np.all(keep)

    #------------------------------ keep nodes far from seam
            init = jigsaw_msh_t()
            init.point = next.point[keep]

            savemsh(OPTS.init_file, init)

    #------------------------------ call JIGSAW with new ICs
        jigsaw (OPTS, next)
 
        cost = metric(next)

        if (cost > best):
    #------------------------------ keep "best" mesh so far!
            mesh = copy.deepcopy(next)
            best = cost

        if (done): return

    return


def attach(mesh):
    """
    ATTACH mark points attached to the underlying geom. rep.

    """

    if (mesh.tria4 is not None and
            mesh.tria4.size != +0):

        mesh.point["IDtag"][mesh.tria4["index"]] = 3

    if (mesh.hexa8 is not None and
            mesh.hexa8.size != +0):

        mesh.point["IDtag"][mesh.hexa8["index"]] = 3

    if (mesh.pyra5 is not None and
            mesh.pyra5.size != +0):

        mesh.point["IDtag"][mesh.pyra5["index"]] = 3

    if (mesh.wedg6 is not None and
            mesh.wedg6.size != +0):

        mesh.point["IDtag"][mesh.wedg6["index"]] = 3

    if (mesh.tria3 is not None and
            mesh.tria3.size != +0):

        mesh.point["IDtag"][mesh.tria3["index"]] = 2

    if (mesh.quad4 is not None and
            mesh.quad4.size != +0):

        mesh.point["IDtag"][mesh.quad4["index"]] = 2

    if (mesh.edge2 is not None and
            mesh.edge2.size != +0):

        mesh.point["IDtag"][mesh.edge2["index"]] = 1

    return


def tetris(opts, nlev, mesh=None):
    """
    TETRIS generate a mesh using an inc. bisection strategy.

    """

    if (not isinstance(opts, jigsaw_jig_t)):
        raise Exception("Incorrect type: OPTS.")

    if (mesh is not None and not
            isinstance(mesh, jigsaw_msh_t)):
        raise Exception("Incorrect type: MESH.")

#---------------------------- call JIGSAW via inc. bisection
    SCAL = +2. ** nlev
    NLEV = nlev
    OPTS = copy.deepcopy(opts)

    while (nlev >= +0):

        if (opts.optm_qlim is not None):

    #------------------------ create/write current QLIM data
            scal = min(
                2.0, (nlev + 1) ** (1. / 4.))

            QLIM = opts.optm_qlim

            OPTS.optm_qlim = QLIM / scal

        else:

            scal = min(
                2.0, (nlev + 1) ** (1. / 4.))

            QLIM = 0.93750

            OPTS.optm_qlim = QLIM / scal

        if (opts.optm_dual is not None):

    #------------------------ create/write current DUAL data
            OPTS.optm_dual = nlev == 0

        if (opts.hfun_hmax is not None):

    #------------------------ create/write current HMAX data
            OPTS.hfun_hmax = \
                opts.hfun_hmax * SCAL

        if (opts.hfun_hmin is not None):

    #------------------------ create/write current HMIN data
            OPTS.hfun_hmin = \
                opts.hfun_hmin * SCAL

        if (opts.hfun_file is not None):

    #------------------------ create/write current HFUN data
            path = Path(opts.hfun_file).parent
            name = Path(opts.hfun_file).stem
            fext = Path(opts.hfun_file).suffix

            name = str(name)
            fext = str(fext)
            name = name + "-ITER" + fext

            OPTS.hfun_file = str(path / name)

            HFUN = jigsaw_msh_t()

            loadmsh(opts.hfun_file, HFUN)

            HFUN.value = HFUN.value * SCAL

            savemsh(OPTS.hfun_file, HFUN)

    #------------------------ call JIGSAW kernel at this lev
        if (nlev % 2 != 0):
        
            ninc = nlev * (-1 + nlev) 

            jitter(OPTS, 3 + ninc, 2, mesh)

        else:

            ninc = nlev * (-1 + nlev)

            jitter(OPTS, 3 + ninc, 3, mesh)

        nlev = nlev - 1
        SCAL = SCAL / 2.

        if (nlev < +0): break

        if (opts.init_file is not None):

    #------------------------ create/write current INIT data
            path = Path(opts.init_file).parent
            name = Path(opts.init_file).stem
            fext = Path(opts.init_file).suffix

            name = str(name)
            fext = str(fext)
            name = name + "-ITER" + fext

            OPTS.init_file = str(path / name)

            bisect(mesh)
            attach(mesh)

            savemsh(OPTS.init_file, mesh)

        else:

    #------------------------ create/write current INIT data
            path = Path(opts.mesh_file).parent
            name = Path(opts.mesh_file).stem
            fext = Path(opts.mesh_file).suffix

            name = str(name)
            fext = str(fext)
            name = name + "-ITER" + fext

            OPTS.init_file = str(path / name)

            bisect(mesh)
            attach(mesh)

            savemsh(OPTS.init_file, mesh)

    return


def refine(opts, nlev, mesh=None):
    """
    REFINE generate a mesh using an inc. bisection strategy.

    """

    if (not isinstance(opts, jigsaw_jig_t)):
        raise Exception("Incorrect type: OPTS.")

    if (mesh is not None and not
            isinstance(mesh, jigsaw_msh_t)):
        raise Exception("Incorrect type: MESH.")

#---------------------------- call JIGSAW via inc. bisection

    opts.mesh_iter = +0
    opts.optm_div_ = False
    opts.optm_zip_ = False

    for ilev in reversed(range(nlev+1)):

        if (opts.optm_dual is not None):

    #------------------------ create/write current DUAL data
            opts.optm_dual = ilev == 0

    #------------------------ call JIGSAW kernel at this lev

        jigsaw(opts, mesh)

        if (ilev <= +0): break

        if (opts.mesh_file is not None):

    #------------------------ create/write current INIT data
            path = Path(opts.mesh_file).parent
            name = Path(opts.mesh_file).stem
            fext = Path(opts.mesh_file).suffix

            name = str(name)
            fext = str(fext)
            name = name + "-ITER" + fext

            opts.init_file = str(path / name)

            bisect(mesh)
            attach(mesh)

            savemsh(opts.init_file, mesh)

    return


def icosahedron(opts, nlev, mesh):
    """
    ICOSAHEDRON Nth-level icosahedral mesh of the ellipsoid.

    """

    if (not isinstance(opts, jigsaw_jig_t)):
        raise Exception("Incorrect type: OPTS.")

    if (not isinstance(mesh, jigsaw_msh_t)):
        raise Exception("Incorrect type: MESH.")

    geom = jigsaw_msh_t()

    loadmsh(opts.geom_file, geom)

#-------------------------------- setup icosahedron geometry
    la = math.atan(0.5)

    lo = 2.0 / 10.0 * np.pi

    PI = np.pi
    mesh.mshID = "euclidean-mesh"
    apos = np.array([
        (+0.0 * PI, -0.5 * PI),
        (+0.0 * PI, +0.5 * PI),
        (+0.0 * lo, +1.0 * la),
        (+1.0 * lo, -1.0 * la),
        (+2.0 * lo, +1.0 * la),
        (+3.0 * lo, -1.0 * la),
        (+4.0 * lo, +1.0 * la),
        (+5.0 * lo, -1.0 * la),
        (+6.0 * lo, +1.0 * la),
        (+7.0 * lo, -1.0 * la),
        (+8.0 * lo, +1.0 * la),
        (+9.0 * lo, -1.0 * la)])

    mesh.vert3 = np.zeros(
        +12, dtype=mesh.VERT3_t)

    mesh.vert3["coord"] = \
        S2toR3(geom.radii, apos)

    mesh.vert3["IDtag"] = -1                # fix "corners"

#-------------------------------- setup icosahedron topology
    mesh.tria3 = np.array([
        ((0,  3,  5),  0),
        ((0,  5,  7),  1),
        ((0,  7,  9),  2),
        ((0,  9, 11),  3),
        ((0, 11,  3),  4),
        ((1,  2,  4),  5),
        ((1,  4,  6),  6),
        ((1,  6,  8),  7),
        ((1,  8, 10),  8),
        ((1, 10,  2),  9),
        ((3,  2,  4), 10),
        ((5,  4,  6), 11),
        ((7,  6,  8), 12),
        ((9,  8, 10), 13),
       ((11, 10,  2), 14),
        ((4,  3,  5), 15),
        ((6,  5,  7), 16),
        ((8,  7,  9), 17),
       ((10,  9, 11), 18),
        ((2, 11,  3), 19)],
        dtype=mesh.TRIA3_t)

    if (nlev <= +0): return

    opts.init_file = opts.mesh_file

    savemsh(opts.init_file, mesh)

    refine(opts, nlev, mesh)

    return


def cubedsphere(opts, nlev, mesh):
    """
    CUBEDSPHERE Nth-level cubedsphere mesh of the ellipsoid.

    """

    if (not isinstance(opts, jigsaw_jig_t)):
        raise Exception("Incorrect type: OPTS.")

    if (not isinstance(mesh, jigsaw_msh_t)):
        raise Exception("Incorrect type: MESH.")

    geom = jigsaw_msh_t()

    loadmsh(opts.geom_file, geom)

#-------------------------------- setup cubedsphere geometry
    aval = math.atan(
        +math.sqrt(+2.0) / +2.0)

    mesh.mshID = "euclidean-mesh"
    apos = np.array([
        (+0.25 * np.pi, -aval),
        (+0.75 * np.pi, -aval),
        (-0.75 * np.pi, -aval),
        (-0.25 * np.pi, -aval),
        (+0.25 * np.pi, +aval),
        (+0.75 * np.pi, +aval),
        (-0.75 * np.pi, +aval),
        (-0.25 * np.pi, +aval)])

    mesh.vert3 = np.zeros(
        + 8, dtype=mesh.VERT3_t)

    mesh.vert3["coord"] = \
        S2toR3(geom.radii, apos)

    mesh.vert3["IDtag"] = -1                # fix "corners"

#-------------------------------- setup cubedsphere topology
    mesh.quad4 = np.array([
        ((0,  1,  2,  3),  0),
        ((0,  1,  5,  4),  1),
        ((1,  2,  6,  5),  2),
        ((2,  3,  7,  6),  3),
        ((3,  0,  4,  7),  4),
        ((4,  5,  6,  7),  5)],
        dtype=mesh.QUAD4_t)

    if (nlev <= +0): return

    opts.init_file = opts.mesh_file

    savemsh(opts.init_file, mesh)

    refine(opts, nlev, mesh)

    return

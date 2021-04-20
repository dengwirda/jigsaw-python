
import numpy as np
from scipy.sparse import csr_matrix

from jigsawpy.tools.predicate import trivol2, trivol3
from jigsawpy.tools.orthoball import tribal2, tribal3
from jigsawpy.tools.scorecard import triscr2, triscr3

from jigsawpy.jig_t import jigsaw_jig_t
from jigsawpy.msh_t import jigsaw_msh_t


def metric(mesh):
    """
    METRIC assemble combined "cost" metric for a given mesh.

    """

    cost = np.empty((+0), dtype=mesh.REALS_t)

    if (mesh.tria3 is not None and
            mesh.tria3.size > +0):

#--------------------------------------- append TRIA3 scores
        COST = triscr2(
            mesh.point["coord"], mesh.tria3["index"]
        )

        cost = np.append(cost, COST)

    if (mesh.tria4 is not None and
            mesh.tria4.size > +0):

#--------------------------------------- append TRIA4 scores
        COST = triscr3(
            mesh.point["coord"], mesh.tria4["index"]
        )

        cost = np.append(cost, COST)

    if (cost.size == 0): return +0.0

    norm = np.sum((1.0 / cost) ** 3)

    return np.cbrt(cost.size / norm)


def jumble(mesh, frac):
    """
    JUMBLE (randomly) perturb a given mesh by fraction FRAC.

    """

    if (mesh.tria3 is not None and
            mesh.tria3.size > +0):

    #-------------------------- quasi-random vert-tria match
        mass = trivol2(
            mesh.point["coord"], mesh.tria3["index"])

        ipos = mesh.tria3["index"].T.ravel()
        jpos = np.arange(0, mesh.tria3.size)
        have = np.unique(ipos)        
        jpos = np.tile(jpos, 3)
        xdat = np.tile(mass, 3)

        xdat = np.random.rand(xdat.size) * xdat
        
        next = np.squeeze(np.asarray(csr_matrix(
            (xdat, (ipos, jpos))).argmax(axis=1)))

    #-------------------------- push toward "matched" centre
        tria = mesh.tria3["index"][next, :]
       
        pmid = tribal2(mesh.point["coord"], tria)
        pmid = pmid[:, :-1]

        pert = np.random.rand(pmid.shape[0], 1)
        pert = 0.50 * (0.50 + pert) * frac
        pert = np.tile(pert, (+1, pmid.shape[1]))

        mesh.point["coord"][have] += \
            pert * (pmid - mesh.point["coord"][have])

    if (mesh.tria4 is not None and
            mesh.tria4.size > +0):

    #-------------------------- quasi-random vert-tria match
        mass = trivol3(
            mesh.point["coord"], mesh.tria4["index"])

        ipos = mesh.tria4["index"].T.ravel()
        jpos = np.arange(0, mesh.tria4.size)
        have = np.unique(ipos)        
        jpos = np.tile(jpos, 4)
        xdat = np.tile(mass, 4)

        xdat = np.random.rand(xdat.size) * xdat
        
        next = np.squeeze(np.asarray(csr_matrix(
            (xdat, (ipos, jpos))).argmax(axis=1)))
        
    #-------------------------- push toward "matched" centre
        tria = mesh.tria4["index"][next, :]
       
        pmid = tribal3(mesh.point["coord"], tria)
        pmid = pmid[:, :-1]

        pert = np.random.rand(pmid.shape[0], 1)
        pert = 0.50 * (0.50 + pert) * frac
        pert = np.tile(pert, (+1, pmid.shape[1]))

        mesh.point["coord"][have] += \
            pert * (pmid - mesh.point["coord"][have])

    attach(mesh)

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


import numpy as np
import warnings
from jigsawpy.msh_t import jigsaw_msh_t
from jigsawpy.tools.scorecard import triscr2, triscr3

class struct(object): pass
class mapper(object):
#------------------------------ obj. to store index mappings
    def __init__(self):
        self.edge2 = struct()
        self.edge2.index = \
    np.empty((0, 0), dtype=np.int32)

        self.tria3 = struct()
        self.tria3.index = \
    np.empty((0, 0), dtype=np.int32)

        self.quad4 = struct()
        self.quad4.index = \
    np.empty((0, 0), dtype=np.int32)

        self.tria4 = struct()
        self.tria4.index = \
    np.empty((0, 0), dtype=np.int32)

        self.hexa8 = struct()
        self.hexa8.index = \
    np.empty((0, 0), dtype=np.int32)

        self.wedg6 = struct()
        self.wedg6.index = \
    np.empty((0, 0), dtype=np.int32)

        self.pyra5 = struct()
        self.pyra5.index = \
    np.empty((0, 0), dtype=np.int32)


def bisect(mesh):
    """
    BISECT: perform uniform bisection of a mesh object.

    """

    if (not isinstance(mesh,jigsaw_msh_t)):
        raise Exception(
            "Incorrect type: MESH.")

    nvrt = +0; vert = None

    if (mesh.vert2 is not None):
        nvrt = nvrt + mesh.vert2.size
    
    if (mesh.vert3 is not None):
        nvrt = nvrt + mesh.vert3.size

    if (nvrt == +0): return

#------------------------------ map elements to unique edges
    edge = np.empty((0,2), dtype=np.int32)
    quad = np.empty((0,4), dtype=np.int32)
    hexa = np.empty((0,8), dtype=np.int32)

    emap = mapper(); qmap = mapper(); hmap = mapper()
    
    if (mesh.edge2 is not None and \
            mesh.edge2.size != +0):
    #-------------------------- map EDGE2's onto JOIN arrays
        nedg = edge.shape[0]
        ncel = mesh.edge2.shape[0]

        cell = mesh.edge2["index"]

        edge = np.concatenate(
            (edge, cell[:,(0,1)]), axis=0)

        emap.edge2.index = \
        np.empty((ncel,1), dtype=np.int32)
        emap.edge2.index[:,0] = \
        np.arange(0,ncel) + ncel*0 + nedg

    if (mesh.tria3 is not None and \
            mesh.tria3.size != +0):
    #-------------------------- map TRIA3's onto JOIN arrays
        nedg = edge.shape[0]
        ncel = mesh.tria3.shape[0]

        cell = mesh.tria3["index"]

        edge = np.concatenate(
            (edge, cell[:,(0,1)]), axis=0)
        edge = np.concatenate(
            (edge, cell[:,(1,2)]), axis=0)
        edge = np.concatenate(
            (edge, cell[:,(2,0)]), axis=0)

        emap.tria3.index = \
        np.empty((ncel,3), dtype=np.int32)
        emap.tria3.index[:,0] = \
        np.arange(0,ncel) + ncel*0 + nedg
        emap.tria3.index[:,1] = \
        np.arange(0,ncel) + ncel*1 + nedg
        emap.tria3.index[:,2] = \
        np.arange(0,ncel) + ncel*2 + nedg

    if (mesh.quad4 is not None and \
            mesh.quad4.size != +0):
    #-------------------------- map QUAD4's onto JOIN arrays
        nedg = edge.shape[0]
        nfac = quad.shape[0]
        ncel = mesh.quad4.shape[0]

        cell = mesh.quad4["index"]

        quad = np.concatenate(
            (quad, cell[:, 0:3 ]), axis=0)

        edge = np.concatenate(
            (edge, cell[:,(0,1)]), axis=0)
        edge = np.concatenate(
            (edge, cell[:,(1,2)]), axis=0)
        edge = np.concatenate(
            (edge, cell[:,(2,3)]), axis=0)
        edge = np.concatenate(
            (edge, cell[:,(3,0)]), axis=0)

        qmap.quad4.index = \
        np.empty((ncel,1), dtype=np.int32)
        qmap.quad4.index[:,0] = \
        np.arange(0,ncel) + ncel*0 + nfac

        emap.quad4.index = \
        np.empty((ncel,4), dtype=np.int32)
        emap.quad4.index[:,0] = \
        np.arange(0,ncel) + ncel*0 + nedg
        emap.quad4.index[:,1] = \
        np.arange(0,ncel) + ncel*1 + nedg
        emap.quad4.index[:,2] = \
        np.arange(0,ncel) + ncel*2 + nedg
        emap.quad4.index[:,3] = \
        np.arange(0,ncel) + ncel*3 + nedg

    if (mesh.tria4 is not None and \
            mesh.tria4.size != +0):
    #-------------------------- map TRIA4's onto JOIN arrays
        nedg = edge.shape[0]
        ncel = mesh.tria4.shape[0]

        cell = mesh.tria4["index"]

        edge = np.concatenate(
            (edge, cell[:,(0,1)]), axis=0)
        edge = np.concatenate(
            (edge, cell[:,(1,2)]), axis=0)
        edge = np.concatenate(
            (edge, cell[:,(2,0)]), axis=0)
        edge = np.concatenate(
            (edge, cell[:,(0,3)]), axis=0)
        edge = np.concatenate(
            (edge, cell[:,(1,3)]), axis=0)
        edge = np.concatenate(
            (edge, cell[:,(2,3)]), axis=0)

        emap.tria4.index = \
        np.empty((ncel,6), dtype=np.int32)
        emap.tria4.index[:,0] = \
        np.arange(0,ncel) + ncel*0 + nedg
        emap.tria4.index[:,1] = \
        np.arange(0,ncel) + ncel*1 + nedg
        emap.tria4.index[:,2] = \
        np.arange(0,ncel) + ncel*2 + nedg
        emap.tria4.index[:,3] = \
        np.arange(0,ncel) + ncel*3 + nedg
        emap.tria4.index[:,4] = \
        np.arange(0,ncel) + ncel*4 + nedg
        emap.tria4.index[:,5] = \
        np.arange(0,ncel) + ncel*5 + nedg

    if (mesh.hexa8 is not None and \
            mesh.hexa8.size != +0):
    #-------------------------- map HEXA8's onto JOIN arrays
        warnings.warn(
        "HEXA-8 currently unsupported", Warning)

    if (mesh.wedg6 is not None and \
            mesh.wedg6.size != +0):
    #-------------------------- map WEDG6's onto JOIN arrays
        warnings.warn(
        "WEDG-6 currently unsupported", Warning)

    if (mesh.pyra5 is not None and \
            mesh.pyra5.size != +0):
    #-------------------------- map PYRA5's onto JOIN arrays
        warnings.warn(
        "PYRA-5 currently unsupported", Warning)        

#------------------------------ unique joins and re-indexing
    if (edge.size != 0):
        __, efwd, erev = np.unique(
            np.sort(edge, axis=1), 
                return_index=True, 
                    return_inverse=True, axis=0)

        edge = edge[efwd,:]

    if (quad.size != 0):
        __, qfwd, qrev = np.unique(
            np.sort(quad, axis=1),
                return_index=True, 
                    return_inverse=True, axis=0)

        quad = quad[qfwd,:]

    if (hexa.size != 0):
        __, hfwd, hrev = np.unique(
            np.sort(hexa, axis=1), 
                return_index=True, 
                    return_inverse=True, axis=0)

        hexa = hexa[hfwd,:]
    
#------------------------------ map unique joins to elements
    if (mesh.edge2 is not None and \
            mesh.edge2.size != +0):
        emap.edge2.index[:,0] = \
            erev[emap.edge2.index[:,0]]
    
    if (mesh.tria3 is not None and \
            mesh.tria3.size != +0):
        emap.tria3.index[:,0] = \
            erev[emap.tria3.index[:,0]]
        emap.tria3.index[:,1] = \
            erev[emap.tria3.index[:,1]]
        emap.tria3.index[:,2] = \
            erev[emap.tria3.index[:,2]]

    if (mesh.quad4 is not None and \
            mesh.quad4.size != +0):
        qmap.quad4.index[:,0] = \
            qrev[emap.quad4.index[:,0]]

        emap.quad4.index[:,0] = \
            erev[emap.quad4.index[:,0]]
        emap.quad4.index[:,1] = \
            erev[emap.quad4.index[:,1]]
        emap.quad4.index[:,2] = \
            erev[emap.quad4.index[:,2]]
        emap.quad4.index[:,3] = \
            erev[emap.quad4.index[:,3]]
    
    if (mesh.tria4 is not None and \
            mesh.tria4.size != +0):
        emap.tria4.index[:,0] = \
            erev[emap.tria4.index[:,0]]
        emap.tria4.index[:,1] = \
            erev[emap.tria4.index[:,1]]
        emap.tria4.index[:,2] = \
            erev[emap.tria4.index[:,2]]
        emap.tria4.index[:,3] = \
            erev[emap.tria4.index[:,3]]
        emap.tria4.index[:,4] = \
            erev[emap.tria4.index[:,4]]
        emap.tria4.index[:,5] = \
            erev[emap.tria4.index[:,5]]

#------------------------------ create new midpoint vertices
    enew = np.empty((0), dtype=np.int32)
    qnew = np.empty((0), dtype=np.int32)
    hnew = np.empty((0), dtype=np.int32)

    if (edge.size != +0):
    #-------------------------- create new vertices for EDGE
        if (mesh.point is not None and \
            mesh.point.size != +0):

            vert = mesh.point["coord"]
            itag = mesh.point["IDtag"]

            emid = vert[edge[:, 0], :] \
                 + vert[edge[:, 1], :]
            emid = emid / +2.

            imid = itag[edge[:, 0]]

            nold = np.size(vert,0)
            nnew = np.size(emid,0)

            enew = nold + np.arange(0,nnew)

            vnew = np.empty((nnew), 
                dtype=mesh.point.dtype)

            vnew["coord"] = emid
            vnew["IDtag"] = imid

            mesh.point = np.concatenate(
                (mesh.point, vnew), axis=0)

    if (quad.size != +0):
    #-------------------------- create new vertices for QUAD
        if (mesh.point is not None and \
            mesh.point.size != +0):

            vert = mesh.point["coord"]
            itag = mesh.point["IDtag"]

            qmid = vert[quad[:, 0], :] \
                 + vert[quad[:, 1], :] \
                 + vert[quad[:, 2], :] \
                 + vert[quad[:, 3], :]
            qmid = qmid / +4.

            imid = itag[quad[:, 0]]

            nold = np.size(vert,0)
            nnew = np.size(qmid,0)

            qnew = nold + np.arange(0,nnew)

            vnew = np.empty((nnew), 
                dtype=mesh.point.dtype)

            vnew["coord"] = qmid
            vnew["IDtag"] = imid

            mesh.point = np.concatenate(
                (mesh.point, vnew), axis=0)

    if (hexa.size != +0):
    #-------------------------- create new vertices for HEXA
        if (mesh.point is not None and \
            mesh.point.size != +0):

            vert = mesh.point["coord"]
            itag = mesh.point["IDtag"]

            hmid = vert[hexa[:, 0], :] \
                 + vert[hexa[:, 1], :] \
                 + vert[hexa[:, 2], :] \
                 + vert[hexa[:, 3], :] \
                 + vert[hexa[:, 4], :] \
                 + vert[hexa[:, 5], :] \
                 + vert[hexa[:, 6], :] \
                 + vert[hexa[:, 7], :]
            hmid = hmid / +8.

            imid = itag[hexa[:, 0]]

            nold = np.size(vert,0)
            nnew = np.size(hmid,0)

            qnew = nold + np.arange(0,nnew)

            vnew = np.empty((nnew), 
                dtype=mesh.point.dtype)

            vnew["coord"] = hmid
            vnew["IDtag"] = imid

            mesh.point = np.concatenate(
                (mesh.point, vnew), axis=0)

    if (mesh.edge2 is not None and \
            mesh.edge2.size != +0):
#------------------------------ create new indexes for EDGE2
        node1 = mesh.edge2["index"][:,0]
        node2 = mesh.edge2["index"][:,1]

        node3 = enew [emap.edge2.index[:,0]]
        
        edgeA = np.empty(
            (mesh.edge2.shape[0]), 
                dtype=jigsaw_msh_t.EDGE2_t)

        edgeA["index"][:,0] = node1
        edgeA["index"][:,1] = node3
        edgeA["IDtag"] = mesh.edge2["IDtag"]

        edgeB = np.empty(
            (mesh.edge2.shape[0]), 
                dtype=jigsaw_msh_t.EDGE2_t)

        edgeB["index"][:,0] = node3
        edgeB["index"][:,1] = node2
        edgeB["IDtag"] = mesh.edge2["IDtag"]

        mesh.edge2 = np.concatenate(
            (edgeA, edgeB), axis=+0)

    if (mesh.tria3 is not None and \
            mesh.tria3.size != +0):
#------------------------------ create new indexes for TRIA3
        node1 = mesh.tria3["index"][:,0]
        node2 = mesh.tria3["index"][:,1]
        node3 = mesh.tria3["index"][:,2]

        node4 = enew [emap.tria3.index[:,0]]
        node5 = enew [emap.tria3.index[:,1]]
        node6 = enew [emap.tria3.index[:,2]]
        
        triaA = np.empty(
            (mesh.tria3.shape[0]), 
                dtype=jigsaw_msh_t.TRIA3_t)

        triaA["index"][:,0] = node1
        triaA["index"][:,1] = node4
        triaA["index"][:,2] = node6
        triaA["IDtag"] = mesh.tria3["IDtag"]

        triaB = np.empty(
            (mesh.tria3.shape[0]), 
                dtype=jigsaw_msh_t.TRIA3_t)

        triaB["index"][:,0] = node2
        triaB["index"][:,1] = node5
        triaB["index"][:,2] = node4
        triaB["IDtag"] = mesh.tria3["IDtag"]

        triaC = np.empty(
            (mesh.tria3.shape[0]), 
                dtype=jigsaw_msh_t.TRIA3_t)

        triaC["index"][:,0] = node3
        triaC["index"][:,1] = node6
        triaC["index"][:,2] = node5
        triaC["IDtag"] = mesh.tria3["IDtag"]

        triaD = np.empty(
            (mesh.tria3.shape[0]), 
                dtype=jigsaw_msh_t.TRIA3_t)

        triaD["index"][:,0] = node4
        triaD["index"][:,1] = node5
        triaD["index"][:,2] = node6
        triaD["IDtag"] = mesh.tria3["IDtag"]

        mesh.tria3 = np.concatenate(
            (triaA, triaB, 
             triaC, triaD), axis=+0)

    if (mesh.quad4 is not None and \
            mesh.quad4.size != +0):
#------------------------------ create new indexes for QUAD4
        node1 = mesh.quad4["index"][:,0]
        node2 = mesh.quad4["index"][:,1]
        node3 = mesh.quad4["index"][:,2]
        node4 = mesh.quad4["index"][:,3]

        node5 = enew [emap.quad4.index[:,0]]
        node6 = enew [emap.quad4.index[:,1]]
        node7 = enew [emap.quad4.index[:,2]]
        node8 = enew [emap.quad4.index[:,3]]
        
        node9 = qnew [qmap.quad4.index[:,0]]

        quadA = np.empty(
            (mesh.quad4.shape[0]), 
                dtype=jigsaw_msh_t.QUAD4_t)

        quadA["index"][:,0] = node1
        quadA["index"][:,1] = node5
        quadA["index"][:,2] = node9
        quadA["index"][:,3] = node8
        quadA["IDtag"] = mesh.quad4["IDtag"]

        quadB = np.empty(
            (mesh.quad4.shape[0]), 
                dtype=jigsaw_msh_t.QUAD4_t)

        quadB["index"][:,0] = node2
        quadB["index"][:,1] = node6
        quadB["index"][:,2] = node9
        quadB["index"][:,3] = node5
        quadB["IDtag"] = mesh.quad4["IDtag"]

        quadC = np.empty(
            (mesh.quad4.shape[0]), 
                dtype=jigsaw_msh_t.QUAD4_t)

        quadC["index"][:,0] = node3
        quadC["index"][:,1] = node7
        quadC["index"][:,2] = node9
        quadC["index"][:,3] = node6
        quadC["IDtag"] = mesh.quad4["IDtag"]

        quadD = np.empty(
            (mesh.quad4.shape[0]), 
                dtype=jigsaw_msh_t.QUAD4_t)

        quadD["index"][:,0] = node4
        quadD["index"][:,1] = node8
        quadD["index"][:,2] = node9
        quadD["index"][:,3] = node7
        quadD["IDtag"] = mesh.quad4["IDtag"]

        mesh.quad4 = np.concatenate(
            (quadA, quadB, 
             quadC, quadD), axis=+0)

    if (mesh.tria4 is not None and \
            mesh.tria4.size != +0):
#------------------------------ create new indexes for TRIA4
        node1 = mesh.tria4["index"][:,0]
        node2 = mesh.tria4["index"][:,1]
        node3 = mesh.tria4["index"][:,2]
        node4 = mesh.tria4["index"][:,3]

        nodeA = enew [emap.tria4.index[:,0]]
        nodeB = enew [emap.tria4.index[:,1]]
        nodeC = enew [emap.tria4.index[:,2]]
        nodeD = enew [emap.tria4.index[:,3]]
        nodeE = enew [emap.tria4.index[:,4]]
        nodeF = enew [emap.tria4.index[:,5]]

        # 1st subdiv. of octahedron
        triaA = np.empty(
            (mesh.tria4.shape[0]), 
                dtype=jigsaw_msh_t.TRIA4_t)

        triaA["index"][:,0] = nodeC
        triaA["index"][:,1] = nodeE
        triaA["index"][:,2] = nodeA
        triaA["index"][:,3] = nodeB
        triaA["IDtag"] = mesh.tria4["IDtag"]

        triaB = np.empty(
            (mesh.tria4.shape[0]), 
                dtype=jigsaw_msh_t.TRIA4_t)

        triaB["index"][:,0] = nodeC
        triaB["index"][:,1] = nodeE
        triaB["index"][:,2] = nodeB
        triaB["index"][:,3] = nodeF
        triaB["IDtag"] = mesh.tria4["IDtag"]

        triaC = np.empty(
            (mesh.tria4.shape[0]), 
                dtype=jigsaw_msh_t.TRIA4_t)

        triaC["index"][:,0] = nodeC
        triaC["index"][:,1] = nodeE
        triaC["index"][:,2] = nodeF
        triaC["index"][:,3] = nodeD
        triaC["IDtag"] = mesh.tria4["IDtag"]

        triaD = np.empty(
            (mesh.tria4.shape[0]), 
                dtype=jigsaw_msh_t.TRIA4_t)

        triaD["index"][:,0] = nodeC
        triaD["index"][:,1] = nodeE
        triaD["index"][:,2] = nodeD
        triaD["index"][:,3] = nodeA
        triaD["IDtag"] = mesh.tria4["IDtag"]

        costA = triscr3( mesh.point["coord"], 
            triaA["index"])
        costB = triscr3( mesh.point["coord"], 
            triaB["index"])
        costC = triscr3( mesh.point["coord"], 
            triaC["index"])
        costD = triscr3( mesh.point["coord"], 
            triaD["index"])

        cost1 = np.minimum(costA, costB)
        cost1 = np.minimum(cost1, costC)
        cost1 = np.minimum(cost1, costD)

        # 2nd subdiv. of octahedron
        triaE = np.empty(
            (mesh.tria4.shape[0]), 
                dtype=jigsaw_msh_t.TRIA4_t)

        triaE["index"][:,0] = nodeA
        triaE["index"][:,1] = nodeF
        triaE["index"][:,2] = nodeE
        triaE["index"][:,3] = nodeB
        triaE["IDtag"] = mesh.tria4["IDtag"]

        triaF = np.empty(
            (mesh.tria4.shape[0]), 
                dtype=jigsaw_msh_t.TRIA4_t)

        triaF["index"][:,0] = nodeA
        triaF["index"][:,1] = nodeF
        triaF["index"][:,2] = nodeB
        triaF["index"][:,3] = nodeC
        triaF["IDtag"] = mesh.tria4["IDtag"]

        triaG = np.empty(
            (mesh.tria4.shape[0]), 
                dtype=jigsaw_msh_t.TRIA4_t)

        triaG["index"][:,0] = nodeA
        triaG["index"][:,1] = nodeF
        triaG["index"][:,2] = nodeC
        triaG["index"][:,3] = nodeD
        triaG["IDtag"] = mesh.tria4["IDtag"]

        triaH = np.empty(
            (mesh.tria4.shape[0]), 
                dtype=jigsaw_msh_t.TRIA4_t)

        triaH["index"][:,0] = nodeA
        triaH["index"][:,1] = nodeF
        triaH["index"][:,2] = nodeD
        triaH["index"][:,3] = nodeE
        triaH["IDtag"] = mesh.tria4["IDtag"]

        costE = triscr3( mesh.point["coord"], 
            triaE["index"])
        costF = triscr3( mesh.point["coord"], 
            triaF["index"])
        costG = triscr3( mesh.point["coord"], 
            triaG["index"])
        costH = triscr3( mesh.point["coord"], 
            triaH["index"])

        cost2 = np.minimum(costE, costF)
        cost2 = np.minimum(cost2, costG)
        cost2 = np.minimum(cost2, costH)

        # 3rd subdiv. of octahedron
        triaI = np.empty(
            (mesh.tria4.shape[0]), 
                dtype=jigsaw_msh_t.TRIA4_t)

        triaI["index"][:,0] = nodeB
        triaI["index"][:,1] = nodeD
        triaI["index"][:,2] = nodeA
        triaI["index"][:,3] = nodeE
        triaI["IDtag"] = mesh.tria4["IDtag"]

        triaJ = np.empty(
            (mesh.tria4.shape[0]), 
                dtype=jigsaw_msh_t.TRIA4_t)

        triaJ["index"][:,0] = nodeB
        triaJ["index"][:,1] = nodeD
        triaJ["index"][:,2] = nodeE
        triaJ["index"][:,3] = nodeF
        triaJ["IDtag"] = mesh.tria4["IDtag"]

        triaK = np.empty(
            (mesh.tria4.shape[0]), 
                dtype=jigsaw_msh_t.TRIA4_t)

        triaK["index"][:,0] = nodeB
        triaK["index"][:,1] = nodeD
        triaK["index"][:,2] = nodeF
        triaK["index"][:,3] = nodeC
        triaK["IDtag"] = mesh.tria4["IDtag"]

        triaL = np.empty(
            (mesh.tria4.shape[0]), 
                dtype=jigsaw_msh_t.TRIA4_t)

        triaL["index"][:,0] = nodeB
        triaL["index"][:,1] = nodeD
        triaL["index"][:,2] = nodeC
        triaL["index"][:,3] = nodeA
        triaL["IDtag"] = mesh.tria4["IDtag"]

        costI = triscr3( mesh.point["coord"], 
            triaI["index"])
        costJ = triscr3( mesh.point["coord"], 
            triaJ["index"])
        costK = triscr3( mesh.point["coord"], 
            triaK["index"])
        costL = triscr3( mesh.point["coord"], 
            triaL["index"])

        cost3 = np.minimum(costI, costJ)
        cost3 = np.minimum(cost3, costK)
        cost3 = np.minimum(cost3, costL)

        # 4 cells in tetra. corners 
        tria1 = np.empty(
            (mesh.tria4.shape[0]), 
                dtype=jigsaw_msh_t.TRIA4_t)

        tria1["index"][:,0] = node1
        tria1["index"][:,1] = nodeA
        tria1["index"][:,2] = nodeC
        tria1["index"][:,3] = nodeD
        tria1["IDtag"] = mesh.tria4["IDtag"]

        tria2 = np.empty(
            (mesh.tria4.shape[0]), 
                dtype=jigsaw_msh_t.TRIA4_t)

        tria2["index"][:,0] = node2
        tria2["index"][:,1] = nodeB
        tria2["index"][:,2] = nodeA
        tria2["index"][:,3] = nodeE
        tria2["IDtag"] = mesh.tria4["IDtag"]

        tria3 = np.empty(
            (mesh.tria4.shape[0]), 
                dtype=jigsaw_msh_t.TRIA4_t)

        tria3["index"][:,0] = node3
        tria3["index"][:,1] = nodeC
        tria3["index"][:,2] = nodeB
        tria3["index"][:,3] = nodeF
        tria3["IDtag"] = mesh.tria4["IDtag"]

        tria4 = np.empty(
            (mesh.tria4.shape[0]), 
                dtype=jigsaw_msh_t.TRIA4_t)

        tria4["index"][:,0] = nodeD
        tria4["index"][:,1] = nodeE
        tria4["index"][:,2] = nodeF
        tria4["index"][:,3] = node4
        tria4["IDtag"] = mesh.tria4["IDtag"]

        # subdiv. with max(min(scr))
        index = np.argsort(np.stack(
            (cost1, cost2, cost3), axis=1), axis=1)

        mesh.tria4 = np.concatenate(
            (tria1, tria2, 
             tria3, tria4,
        # 1st subdiv. of octahedron
             triaA[index[:,2] == 0],
             triaB[index[:,2] == 0],
             triaC[index[:,2] == 0],
             triaD[index[:,2] == 0],
        # 2nd subdiv. of octahedron
             triaE[index[:,2] == 1],
             triaF[index[:,2] == 1],
             triaG[index[:,2] == 1],
             triaH[index[:,2] == 1],
        # 3rd subdiv. of octahedron
             triaI[index[:,2] == 2],
             triaJ[index[:,2] == 2],
             triaK[index[:,2] == 2],
             triaL[index[:,2] == 2]
            ), axis = +0 )

    return




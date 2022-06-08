
import ctypes as ct

from jigsawpy.def_t import indx_t, real_t


#---------------------------- ctypes struct for JIGSAW's API

class libsaw_jig_t(ct.Structure):
    _fields_ = [

    # VERBOSITY - {default=0} verbosity of log-file gene-
    # rated by JIGSAW. Set VERBOSITY > 0 for more output.

    ("verbosity", indx_t),

    # GEOM-SEED - {default = 8} number of "seed" vertices
    # used to initialise mesh generation.

    ("geom_seed", indx_t),

    # GEOM_FEAT - {default = false} attempt to auto-detect
    # "sharp-features" in the input geometry. Features can
    # lie adjacent to 1-dim. entities, (i.e. geometry
    # "edges") and/or 2-dim. entities, (i.e. geometry
    # "faces") based on both geometrical and/or topologic-
    # al constraints. Geometrically, features are located
    # between any neighbouring entities that subtend
    # angles less than GEOM_ETAX degrees, where "X" is the
    # (topological) dimension of the feature. Topological-
    # ly, features are located at the apex of any non-man-
    # ifold connections.

    ("geom_feat", indx_t),

    # GEOM_ETA1 - {default = 45deg} 1-dim. feature-angle,
    # features are located between any neighbouring
    # "edges" that subtend angles less than ETA1 deg.

    ("geom_eta1", real_t),

    # GEOM_ETA2 - {default = 45deg} 2-dim. feature-angle,
    # features are located between any neighbouring
    # "faces" that subtend angles less than ETA2 deg.

    ("geom_eta2", real_t),

    # INIT_NEAR - {default = 1.E-8} relative "zip" tol.
    # applied when processing initial conditions. In cases
    # where "sharp-feature" detection is active, nodes in
    # the initial set are zipped to their nearest feature
    # node if the separation length is less than NEAR*SCAL
    # where SCAL is the max. bounding-box dimension.

    ("init_near", real_t),

    # HFUN_SCAL - {default = 'relative'} scaling type for
    # mesh-size fuction. HFUN_SCAL='relative' interprets
    # mesh-size values as percentages of the (mean) length
    # of the axis-aligned bounding-box (AABB) associated
    # with the geometry. HFUN_SCAL = 'absolute' interprets
    # mesh-size values as absolute measures.

    ("hfun_scal", indx_t),

    # HFUN_HMAX - {default = 0.02} max. mesh-size function
    # value. Interpreted based on SCAL setting.

    ("hfun_hmax", real_t),

    # HFUN_HMIN - {default = 0.00} min. mesh-size function
    # value. Interpreted based on SCAL setting.

    ("hfun_hmin", real_t),

    # BNDS_KERN - {default = 'bnd-tria'} placement of bou-
    # ndary, enforcing conformance w.r.t the triangulation
    # (KERN='bnd-tria') or w.r.t the dual voronoi complex
    # (KERN='bnd-dual').

    ("bnds_kern", indx_t),

    # MESH_DIMS - {default=+3} number of "topological" di-
    # mensions to mesh. DIMS=K meshes K-dimensional featu-
    # res, irrespective of the number of spatial dim.'s of
    # the problem (i.e. if the geometry is 3-dimensional
    # and DIMS=2 a surface mesh will be produced).

    ("mesh_dims", indx_t),

    # MESH_KERN - {default = 'delfront'} meshing kernal,
    # choice of the standard Delaunay-refinement algorithm
    # (KERN='delaunay') or the Frontal-Delaunay method
    # (KERN='delfront').

    ("mesh_kern", indx_t),

    # MESH_ITER - {default = INF} max. number of mesh ref-
    # inement iterations. Set ITER=N to see progress after
    # N iterations.

    ("mesh_iter", indx_t),

    # MESH_TOP1 - {default=false} enforce 1-dim. topolog-
    # ical constraints. 1-dim. edges are refined until all
    # embedded nodes are "locally 1-manifold", i.e. nodes
    # are either centred at topological "features", or lie
    # on 1-manifold complexes.

    ("mesh_top1", indx_t),

    # MESH_TOP2 - {default=false} enforce 2-dim. topolog-
    # ical constraints. 2-dim. trias are refined until all
    # embedded nodes are "locally 2-manifold", i.e. nodes
    # are either centred at topological "features", or lie
    # on 2-manifold complexes.

    ("mesh_top2", indx_t),

    # MESH_RAD2 - {default = 1.05} max. radius-edge ratio
    # for 2-tria elements. 2-trias are refined until the
    # ratio of the element circumradii to min. edge length
    # is less-than RAD2.

    ("mesh_rad2", real_t),

    # MESH_RAD3 - {default = 2.05} max. radius-edge ratio
    # for 3-tria elements. 3-trias are refined until the
    # ratio of the element circumradii to min. edge length
    # is less-than RAD3.

    ("mesh_rad3", real_t),

    # MESH_SIZ1 - {default=4/3+eps} h(x)-based refinement
    # multiplier for 1-dimensional elements. Edges are
    # refined if they are locally larger than SIZ1 * h(x).

    ("mesh_siz1", real_t),

    # MESH_SIZ2 - {default=4/3+eps} h(x)-based refinement
    # multiplier for 2-dimensional elements. Cells are
    # refined if they are locally larger than SIZ2 * h(x).

    ("mesh_siz2", real_t),

    # MESH_SIZ3 - {default=4/3+eps} h(x)-based refinement
    # multiplier for 3-dimensional elements. Cells are
    # refined if they are locally larger than SIZ3 * h(x).

    ("mesh_siz3", real_t),

    # MESH_OFF2 - {default=0.90} radius-edge ratio target
    # for insertion of "shape"-type offcentres for 2-tria
    # elements. When refining an element II, offcentres
    # are positioned to form a new "frontal" element JJ
    # that satisfies JRAD <= OFF2.

    ("mesh_off2", real_t),

    # MESH_OFF3 - {default=1.10} radius-edge ratio target
    # for insertion of "shape"-type offcentres for 3-tria
    # elements. When refining an element II, offcentres
    # are positioned to form a new "frontal" element JJ
    # that satisfies JRAD <= OFF3.

    ("mesh_off3", real_t),

    # MESH_SNK2 - {default=0.20} inflation tolerance for
    # insertion of "sink" offcentres for 2-tria elements.
    # When refining an element II, "sinks" are positioned
    # at the centre of the largest adj. circumball staisf-
    # ying |JBAL-IBAL| < SNK2 * IRAD, where IRAD is the
    # radius of the circumball, and [IBAL,JBAL] are the
    # circumball centres.

    ("mesh_snk2", real_t),

    # MESH_SNK3 - {default=0.33} inflation tolerance for
    # insertion of "sink" offcentres for 3-tria elements.
    # When refining an element II, "sinks" are positioned
    # at the centre of the largest adj. circumball staisf-
    # ying |JBAL-IBAL| < SNK3 * IRAD, where IRAD is the
    # radius of the circumball, and [IBAL,JBAL] are the
    # circumball centres.

    ("mesh_snk3", real_t),

    # MESH_EPS1 - {default=0.33} max. surface-discretisa-
    # tion error multiplier for 1-edge elements. 1-edge
    # elements are refined until the surface-disc. error
    # is less-than EPS1 * HFUN(X).

    ("mesh_eps1", real_t),

    # MESH_EPS2 - {default=0.33} max. surface-discretisa-
    # tion error multiplier for 2-tria elements. 2-tria
    # elements are refined until the surface-disc. error
    # is less-than EPS2 * HFUN(X).

    ("mesh_eps2", real_t),

    # MESH_VOL3 - {default=0.00} min. volume-length ratio
    # for 3-tria elements. 3-tria elements are refined
    # until the volume-length ratio exceeds VOL3. Can be
    # used to supress "sliver" elements.

    ("mesh_vol3", real_t),

    # OPTM_KERN - {default = 'odt+dqdx'} mesh optimisation
    # kernel, choice of an Optimal Delaunay Tessellation
    # strategy (KERN='odt+dqdx') or a Centroidal Voronoi
    # Tessellation method (KERN='cvt+dqdx'). In both cases
    # a hybrid formulation is employed, using a "blend" of
    # ODT/CVT updates, and gradients of a "fall-back" mesh
    # quality function Q.

    ("optm_kern", indx_t),

    # OPTM_ITER - {default=16} max. number of mesh optimi-
    # sation iterations. Set ITER=N to see progress after
    # N iterations.

    ("optm_iter", indx_t),

    # OPTM_COST - {default='area-len'} mesh optimisation
    # cost metric, choice of area-length (COST='area-len') 
    # or skewed-cosine (COST='skew-cos') functions.
    # The area-length metric is symmetric wrt. both small 
    # and large cell angles, and is typically appropriate
    # for simplex-only meshes. The skewed-cosine metric 
    # is based on an asymmetric penalisation of large cell
    # angles, and may be useful for staggered primal-dual 
    # tessellations.

    ("optm_cost", indx_t),

    # OPTM_QTOL - {default=1.E-04} tolerance on mesh cost
    # function for convergence. Iteration on a given node
    # is terminated if adjacent element cost-functions are
    # improved by less than QTOL.

    ("optm_qtol", real_t),

    # OPTM_QLIM - {default=0.9375} threshold on mesh cost
    # function above which gradient-based optimisation is
    # attempted.

    ("optm_qlim", real_t),

    # OPTM_TRIA - {default= true} allow for optimisation
    # of TRIA grid geometry.

    ("optm_tria", indx_t),

    # OPTM_DUAL - {default=false} allow for optimisation
    # of DUAL grid geometry.

    ("optm_dual", indx_t),

    # OPTM_ZIP_ - {default= true} allow for "merge" oper-
    # ations on sub-faces within the optimisation stages.

    ("optm_zip_", indx_t),

    # OPTM_DIV_ - {default= true} allow for "split" oper-
    # ations on sub-faces within the optimisation stages.

    ("optm_div_", indx_t)]


import ctypes as ct

from jigsawpy.def_t import indx_t, real_t

#------------------------------------------- POINT struct.'s

class libsaw_VERT2_t(ct.Structure):
    _fields_ = [("ppos", real_t*2), 
                ("itag", indx_t)
               ]

class libsaw_VERT2_array_t(ct.Structure):
    _fields_ = [("size", indx_t),
                ("data", \
              ct.POINTER(libsaw_VERT2_t))
               ]

class libsaw_VERT3_t(ct.Structure):
    _fields_ = [("ppos", real_t*3), 
                ("itag", indx_t)
               ]

class libsaw_VERT3_array_t(ct.Structure):
    _fields_ = [("size", indx_t),
                ("data", \
              ct.POINTER(libsaw_VERT3_t))
               ]

#------------------------------------------- 1-CEL struct.'s

class libsaw_EDGE2_t(ct.Structure):
    _fields_ = [("node", indx_t*2), 
                ("itag", indx_t)
               ]

class libsaw_EDGE2_array_t(ct.Structure):
    _fields_ = [("size", indx_t),
                ("data", \
              ct.POINTER(libsaw_EDGE2_t))
               ]

#------------------------------------------- 2-CEL struct.'s

class libsaw_TRIA3_t(ct.Structure):
    _fields_ = [("node", indx_t*3), 
                ("itag", indx_t)
               ]

class libsaw_TRIA3_array_t(ct.Structure):
    _fields_ = [("size", indx_t),
                ("data", \
              ct.POINTER(libsaw_TRIA3_t))
               ]

class libsaw_QUAD4_t(ct.Structure):
    _fields_ = [("node", indx_t*4), 
                ("itag", indx_t)
               ]

class libsaw_QUAD4_array_t(ct.Structure):
    _fields_ = [("size", indx_t),
                ("data", \
              ct.POINTER(libsaw_QUAD4_t))
               ]

#------------------------------------------- 3-CEL struct.'s

class libsaw_TRIA4_t(ct.Structure):
    _fields_ = [("node", indx_t*4), 
                ("itag", indx_t)
               ]

class libsaw_TRIA4_array_t(ct.Structure):
    _fields_ = [("size", indx_t),
                ("data", \
              ct.POINTER(libsaw_TRIA4_t))
               ]

class libsaw_HEXA8_t(ct.Structure):
    _fields_ = [("node", indx_t*8), 
                ("itag", indx_t)
               ]

class libsaw_HEXA8_array_t(ct.Structure):
    _fields_ = [("size", indx_t),
                ("data", \
              ct.POINTER(libsaw_HEXA8_t))
               ]

class libsaw_WEDG6_t(ct.Structure):
    _fields_ = [("node", indx_t*6), 
                ("itag", indx_t)
               ]

class libsaw_WEDG6_array_t(ct.Structure):
    _fields_ = [("size", indx_t),
                ("data", \
              ct.POINTER(libsaw_WEDG6_t))
               ]

class libsaw_PYRA5_t(ct.Structure):
    _fields_ = [("node", indx_t*5), 
                ("itag", indx_t)
               ]

class libsaw_PYRA5_array_t(ct.Structure):
    _fields_ = [("size", indx_t),
                ("data", \
              ct.POINTER(libsaw_PYRA5_t))
               ]

#------------------------------------------- BOUND struct.'s

class libsaw_BOUND_t(ct.Structure):
    _fields_ = [("itag", indx_t),
                ("indx", indx_t), 
                ("kind", indx_t)
               ]

class libsaw_BOUND_array_t(ct.Structure):
    _fields_ = [("size", indx_t),
                ("data", \
              ct.POINTER(libsaw_BOUND_t))
               ]

#------------------------------------------- MISC. struct.'s

class libsaw_REALS_array_t(ct.Structure):
    _fields_ = [("size", indx_t),
                ("data", \
              ct.POINTER(real_t))
               ]

class libsaw_INDEX_array_t(ct.Structure):
    _fields_ = [("size", indx_t),
                ("data", \
              ct.POINTER(indx_t))
               ]

#---------------------------- ctypes struct for JIGSAW's API

class libsaw_msh_t(ct.Structure):
    _fields_ = [("flags",indx_t),

    # VERT2 - 2-dim. vertex coordinates
    # VERT2 is an array of libsaw_VERT2_t struct.'s, where:
    # VERT2.DATA[:].PPOS is an array of coordinate values,
    # VERT2.DATA[:].ITAG is an array of associated ID tags.

    ("vert2",libsaw_VERT2_array_t),

    # VERT3 - 3-dim. vertex coordinates
    # VERT3 is an array of libsaw_VERT3_t struct.'s, where:
    # VERT3.DATA[:].PPOS is an array of coordinate values,
    # VERT3.DATA[:].ITAG is an array of associated ID tags.

    ("vert3",libsaw_VERT3_array_t),

    # POWER - vertex "weights" associated with dual "power" 
    # tessellation.

    ("power",libsaw_REALS_array_t),

    # EDGE2 - EDGE-2 element definitions
    # EDGE2 is an array of libsaw_EDGE2_t struct.'s, where:
    # EDGE2.DATA[:].NODE is an array of element indexing,
    # EDGE2.DATA[:].ITAG is an array of associated ID tags.

    ("edge2",libsaw_EDGE2_array_t),

    # TRIA3 - TRIA-3 element definitions
    # TRIA3 is an array of libsaw_TRIA3_t struct.'s, where:
    # TRIA3.DATA[:].NODE is an array of element indexing,
    # TRIA3.DATA[:].ITAG is an array of associated ID tags.

    ("tria3",libsaw_TRIA3_array_t),

    # QUAD4 - QUAD-4 element definitions
    # QUAD4 is an array of libsaw_QUAD4_t struct.'s, where:
    # QUAD4.DATA[:].NODE is an array of element indexing,
    # QUAD4.DATA[:].ITAG is an array of associated ID tags.

    ("quad4",libsaw_QUAD4_array_t),

    # TRIA4 - TRIA-4 element definitions
    # TRIA4 is an array of libsaw_TRIA4_t struct.'s, where:
    # TRIA4.DATA[:].NODE is an array of element indexing,
    # TRIA4.DATA[:].ITAG is an array of associated ID tags.    

    ("tria4",libsaw_TRIA4_array_t),

    # HEXA8 - HEXA-8 element definitions
    # HEXA8 is an array of libsaw_HEXA8_t struct.'s, where:
    # HEXA8.DATA[:].NODE is an array of element indexing,
    # HEXA8.DATA[:].ITAG is an array of associated ID tags.

    ("hexa8",libsaw_HEXA8_array_t),

    # WEDG6 - WEDG-6 element definitions
    # WEDG6 is an array of libsaw_WEDG6_t struct.'s, where:
    # WEDG6.DATA[:].NODE is an array of element indexing,
    # WEDG6.DATA[:].ITAG is an array of associated ID tags.

    ("wedg6",libsaw_WEDG6_array_t),

    # PYRA5 - PYRA-5 element definitions
    # PYRA5 is an array of libsaw_PYRA5_t struct.'s, where:
    # PYRA5.DATA[:].NODE is an array of element indexing,
    # PYRA5.DATA[:].ITAG is an array of associated ID tags.

    ("pyra5",libsaw_PYRA5_array_t),
    
    # BOUND - "boundary" indexing,
    # BOUND is an array of libsaw_BOUND_t struct.'s, which
    # describe how elements in the geometry are associated 
    # with enclosed areas/volumes, herein known as "parts":
    # BOUND.DATA[:].INDX is an array of cell indexing,        
    # BOUND.DATA[:].KIND is an array of cell tags, defining 
    # which element "kind" is indexed via BOUND.DATA.INDX
    # BOUND.DATA[:].ITAG is an array of associated ID tags.
 
    ("bound",libsaw_BOUND_array_t),

    # RADII - 3-by-1 array of principal ellipsoid radii.

    ("radii",libsaw_REALS_array_t),

    # KGRID - array of "k-axis" grid coordinates for "grid"
    # type objects. Coordinates must vary monotonically.

    ("xgrid",libsaw_REALS_array_t),
    ("ygrid",libsaw_REALS_array_t),
    ("zgrid",libsaw_REALS_array_t),

    # VALUE - "values" associated with the vertices of the 
    # mesh object.

    ("value",libsaw_REALS_array_t),

    # SLOPE - "slopes" associated with the vertices of the 
    # mesh object.

    ("slope",libsaw_REALS_array_t)]




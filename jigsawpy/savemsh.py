
from pathlib import Path

from jigsawpy.msh_t import jigsaw_msh_t

from jigsawpy.parse.savemsh import savemsh as _savemsh
from jigsawpy.parse.save_nc import save_nc as _save_nc


def savemsh(name, mesh):
    """
    SAVEMSH: save a JIGSAW MSH object to file.

    SAVEMSH(NAME, MESH)

    MESH is JIGSAW's primary mesh/grid/geom class. See MSH_t
    for details.

    Data in MESH is written as-needed -- any objects defined
    will be saved to file.

    For NetCDF grids, VALUE and SLOPE use dimensions (x),
    (x, y), or (z, x, y), preserving y-fast ordering.
    Mesh fields use the vertex-row dimension; a shared scalar
    slope is stored separately.
    Radius-only ellipsoid meshes default to NDIMS=3 when
    MESH.NDIMS is unspecified.

    """
    if (not isinstance(name, str)):
        raise TypeError("Incorrect type: NAME.")

    if (not isinstance(mesh, jigsaw_msh_t)):
        raise TypeError("Incorrect type: MESH.")

    if Path(name).suffix.lower() == ".nc":
        _save_nc(name, mesh)
    else:
        _savemsh(name, mesh)

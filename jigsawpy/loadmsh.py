
from pathlib import Path

from jigsawpy.msh_t import jigsaw_msh_t

from jigsawpy.parse.loadmsh import loadmsh as _loadmsh
from jigsawpy.parse.load_nc import load_nc as _load_nc


def loadmsh(name, mesh):
    """
    LOADMSH: load a JIGSAW MSH obj. from file.

    LOADMSH(NAME, MESH)

    MESH is JIGSAW's primary mesh/grid/geom class. See MSH_t
    for details.

    Data in MESH is loaded on-demand -- any objects included
    in the file will be read.

    """
    if (not isinstance(name, str)):
        raise TypeError("Incorrect type: NAME.")

    if (not isinstance(mesh, jigsaw_msh_t)):
        raise TypeError("Incorrect type: MESH.")

    if Path(name).suffix.lower() == ".nc":
        _load_nc(name, mesh)
    else:
        _loadmsh(name, mesh)

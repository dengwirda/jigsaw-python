
import numpy as np
import json
import argparse

from jigsawpy import jigsaw_msh_t, savemsh


def linegeo(line, nset, eset, nobj, last):
    """
    LINEGEO: read a geoJSON line into a jigsaw msh_t object.

    """

    npts = len(line) - 0

    if (npts > 0):
#----------------------------------------- read LINE dataset
        temp = jigsaw_msh_t()
        temp.vert2 = np.zeros(
            (npts + 0), dtype=temp.VERT2_t)
        temp.edge2 = np.zeros(
            (npts - 1), dtype=temp.EDGE2_t)

        temp.edge2["IDtag"][:] = nobj

        nobj = nobj + 1

        indx = np.arange(0, npts - 1) + last

        last = last + npts

        temp.vert2["coord"] = line[+0::]

        temp.edge2["index"][:, 0] = indx + 0
        temp.edge2["index"][:, 1] = indx + 1

        nset.append(temp.vert2)
        eset.append(temp.edge2)

    return nobj, last


def polygeo(loop, nset, eset, nobj, last):
    """
    POLYGEO: read a geoJSON poly into a jigsaw msh_t object.

    """

    npts = len(loop) - 1

    if (npts > +0):
#----------------------------------------- read LOOP dataset
        temp = jigsaw_msh_t()
        temp.vert2 = np.zeros(
            (npts + 0), dtype=temp.VERT2_t)
        temp.edge2 = np.zeros(
            (npts - 0), dtype=temp.EDGE2_t)

        temp.edge2["IDtag"][:] = nobj

        nobj = nobj + 1

        indx = np.arange(0, npts - 1) + last

        itop = last + npts - 1

        idx1 = np.full(
            npts, itop, dtype=np.int32)
        idx1[:-1] = indx + 0

        idx2 = np.full(
            npts, last, dtype=np.int32)
        idx2[:-1] = indx + 1

        last = last + npts

        temp.vert2["coord"] = loop[:-1:]

        temp.edge2["index"][:, 0] = idx1
        temp.edge2["index"][:, 1] = idx2

        nset.append(temp.vert2)
        eset.append(temp.edge2)

    return nobj, last


def readgeo(geom, nset, eset, nobj, last):
    """
    READGEO: read a geoJSON part into a jigsaw msh_t object.

    """

    if   (geom["type"] == "LineString"):

        line = geom["coordinates"]

        nobj, last = linegeo(
            line, nset, eset, nobj, last)

    elif (geom["type"] == "MultiLineString"):

        for line in geom["coordinates"]:

            nobj, last = linegeo(
                line, nset, eset, nobj, last)

    elif (geom["type"] == "Polygon"):

        for loop in geom["coordinates"]:

            nobj, last = polygeo(
                loop, nset, eset, nobj, last)

    elif (geom["type"] == "MultiPolygon"):

        for poly in geom["coordinates"]:
            for loop in poly:

                nobj, last = polygeo(
                    loop, nset, eset, nobj, last)

    return nobj, last


def loadgeo(name, mesh):
    """
    LOADGEO: load a geoJSON file into a jigsaw msh_t object.

    """

    if (not isinstance(name, str)):
        raise Exception("Incorrect type: NAME.")

    if (not isinstance(mesh, jigsaw_msh_t)):
        raise Exception("Incorrect type: MESH.")

    nobj = +0; last = +0; nset = []; eset = []

    with open(name) as f: geoj = json.load(f)

    for feat in geoj["features"]:

        geom = (feat["geometry"])

        if (geom["type"] != "GeometryCollection"):

            nobj, last = readgeo(
                geom, nset, eset, nobj, last)

        else:

            for next in geom["geometries"]:

                nobj, last = readgeo(
                    next, nset, eset, nobj, last)

    mesh.vert2 = np.concatenate(nset, axis=0)
    mesh.edge2 = np.concatenate(eset, axis=0)

    return


if (__name__ == "__main__"):
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument(
        "--src-file", dest="src_file", type=str,
        required=True, help="src geoJSON file to load")

    parser.add_argument(
        "--dst-file", dest="dst_file", type=str,
        required=True, help="Output .msh file to save")

    args = parser.parse_args()

    mesh = jigsaw_msh_t()

    loadgeo(name=args.src_file, mesh=mesh)
    savemsh(name=args.dst_file, mesh=mesh)


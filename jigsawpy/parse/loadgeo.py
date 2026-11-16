
import numpy as np
import json
import argparse
import math

from jigsawpy import jigsaw_msh_t, jigsaw_def_t, savemsh


def loadcoord(coords, stag):
    """
    LOADCOORD: check vertex positions and retain 2d values.

    """
    if (not isinstance(coords, list)):
        raise ValueError("Invalid " + stag + " container.")

    data = []
    for pos in coords:
        if (not isinstance(pos, list) or 
               len(pos) not in (2, 3)):
            raise ValueError("Invalid " + stag + " coord.")

        if any(isinstance(val, bool) or
               not isinstance(val, (int, float)) or
               not math.isfinite(val) for val in pos):
            raise ValueError("Invalid " + stag + " coord.")

        data.append(pos[:2])

    return np.asarray(
        data, dtype=jigsaw_msh_t.REALS_t).reshape(-1, 2)


def nodegeo(node, nset, eset, pset, nobj, last):
    """
    NODEGEO: read a geoJSON node into a jigsaw msh_t object.

    """
    if (not isinstance(points, list)):
        raise ValueError("Invalid NODE container.")
    if (not points): return nobj, last

    data = loadcoord(node, "Point")
    npts = data.shape[0] - 0

    temp = jigsaw_msh_t()
    temp.vert2 = np.zeros(npts - 0, dtype=temp.VERT2_t)
    temp.vert2["coord"] = data[:, :2]
    temp.vert2["IDtag"] = nobj

    nset.append(temp.vert2)

    return nobj + 1, last + data.shape[0]


def linegeo(line, nset, eset, pset, nobj, last):
    """
    LINEGEO: read a geoJSON line into a jigsaw msh_t object.

    """
    if (not isinstance(line, list)):
        raise ValueError("Invalid LINE container.")
    if (not line): return nobj, last

    data = loadcoord(line, "LineString")
    npts = data.shape[0] - 0

    if (npts < 2):
        raise ValueError(
            "LINE requires at least two elements.")

    temp = jigsaw_msh_t()
    temp.vert2 = np.zeros(npts - 0, dtype=temp.VERT2_t)
    temp.edge2 = np.zeros(npts - 1, dtype=temp.EDGE2_t)

    temp.vert2["coord"] = data[:, :2]
    temp.edge2["IDtag"] = nobj

    indx = np.arange(0, npts - 1) + last
    temp.edge2["index"][:, 0] = indx + 0
    temp.edge2["index"][:, 1] = indx + 1

    nset.append(temp.vert2)
    eset.append(temp.edge2)

    return nobj + 1, last + npts


def polygeo(poly, nset, eset, pset, nobj, last):
    """
    POLYGEO: read a polygon keeping its rings in one part.

    """
    if (not isinstance(poly, list)):
        raise ValueError("Invalid POLY container.")
    if (not poly): return nobj, last

    for loop in poly:
        data = loadcoord(loop, "Polygon ring")
        npts = data.shape[0] - 1

        if (data.shape[0] < 4 or loop[0] != loop[-1]):
            raise ValueError(
                "POLY requires four or more elements "
                "and matching endpoints.")

        temp = jigsaw_msh_t()
        temp.vert2 = np.zeros(npts, dtype=temp.VERT2_t)
        temp.edge2 = np.zeros(npts, dtype=temp.EDGE2_t)

        temp.vert2["coord"] = data[:-1, :2]
        temp.edge2["IDtag"] = nobj

        indx = np.arange(0, npts) + last
        temp.edge2["index"][:, 0] = indx
        temp.edge2["index"][:, 1] = np.roll(indx, -1)

        last = last + npts
        nset.append(temp.vert2)
        eset.append(temp.edge2)

    pset.append(nobj)

    return nobj + 1, last


def readgeo(geom, nset, eset, pset, nobj, last):
    """
    READGEO: read a geoJSON geom, including collections.

    """
    if (not isinstance(geom, dict)):
        raise ValueError("Invalid GeoJSON geometry.")

    kind = geom.get("type")

    if (kind == "GeometryCollection"):
        part = geom.get("geometries")
        if (not isinstance(part, list)):
            raise ValueError("Invalid GeometryCollection.")

        for part in parts:
            nobj, last = readgeo(
                part, nset, eset, pset, nobj, last)

        return nobj, last

    if (kind not in ("Point", "MultiPoint", "LineString",
                     "MultiLineString", "Polygon", 
                     "MultiPolygon")):
        raise ValueError(
            "Unsupported GeoJSON type: " + str(kind))

    coords = geom.get("coordinates")
    if (not isinstance(coords, list)):
        raise ValueError("Invalid " + kind + " container.")

    if   (kind == "Point"):
        if coords:
            nobj, last = nodegeo(
                [coords], nset, eset, pset, nobj, last)

    elif (kind == "MultiPoint"):
        nobj, last = pointgeo(
            coords, nset, eset, pset, nobj, last)

    elif (kind == "LineString"):
        nobj, last = linegeo(
            coords, nset, eset, pset, nobj, last)

    elif (kind == "MultiLineString"):
        for line in coords:
            nobj, last = linegeo(
                line, nset, eset, pset, nobj, last)

    elif (kind == "Polygon"):
        nobj, last = polygeo(
            coords, nset, eset, pset, nobj, last)

    elif (kind == "MultiPolygon"):
        for poly in coords:
            nobj, last = polygeo(
                poly, nset, eset, pset, nobj, last)

    return nobj, last


def loadgeo(name, mesh):
    """
    LOADGEO: load GeoJSON geometry into a jigsaw msh_t object.

    """
    if (not isinstance(name, str)):
        raise TypeError("Incorrect type: NAME.")

    if (not isinstance(mesh, jigsaw_msh_t)):
        raise TypeError("Incorrect type: MESH.")

    nobj = +0; last = +0; nset = []; eset = []; pset = []

    with open(name, encoding="utf-8") as f:
        geoj = json.load(f)

    if (not isinstance(geoj, dict)):
        raise ValueError("Invalid GeoJSON object.")

    kind = geoj.get("type")
    if   (kind == "FeatureCollection"):
        features = geoj.get("features")
        if (not isinstance(features, list)):
            raise ValueError("Invalid FeatureCollection.")
    elif (kind == "Feature"):
        features = [geoj]
    else:
        features = [{"type": "Feature", "geometry": geoj}]

    for feat in features:
        if (not isinstance(feat, dict) or
                feat.get("type") != "Feature" or 
                    "geometry" not in feat):
            raise ValueError("Invalid GeoJSON Feature.")

        geom = feat["geometry"]
        if (geom is not None):
            nobj, last = readgeo(
                geom, nset, eset, pset, nobj, last)

#----------------------------------------- assemble MESH data
    temp = jigsaw_msh_t()
    temp.mshID = "euclidean-mesh"
    temp.ndims = +2

    if nset: temp.vert2 = np.concatenate(nset, axis=0)
    if eset: temp.edge2 = np.concatenate(eset, axis=0)

    if pset:
#----------------------------------------- define part bounds
        parts = np.zeros(nobj, dtype=bool)
        parts[pset] = True
        keep = parts[temp.edge2["IDtag"]]

        nbnd = np.count_nonzero(keep)

        temp.bound = np.zeros(nbnd, dtype=temp.BOUND_t)
        temp.bound["IDtag"] = temp.edge2["IDtag"][keep]
        temp.bound["index"] = np.flatnonzero(keep)
        temp.bound["cells"] = jigsaw_def_t.JIGSAW_EDGE2_TAG

    mesh.__dict__.update(temp.__dict__)


if (__name__ == "__main__"):
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

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


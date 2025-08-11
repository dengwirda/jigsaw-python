
from pathlib import Path
from jigsawpy.prj_t import jigsaw_prj_t


def savechar(fptr, sval, stag):

    if (isinstance(sval, str)):
        fptr.write("  " + stag + "=" + sval + "\n")
    else:
        raise TypeError(
            "Invalid [CHARA] data: OPTS." + stag)

    return


def saveints(fptr, ival, stag):

    if (isinstance(ival, int)):
        fptr.write(
            "  " + stag + "=" + str(ival) + "\n")
    else:
        raise TypeError(
            "Invalid [INDEX] data: OPTS." + stag)

    return


def savereal(fptr, fval, stag):

    if (isinstance(fval, float)):
        fptr.write(
            "  " + stag + "=" + str(fval) + "\n")
    else:
        raise TypeError(
            "Invalid [FLOAT] data: OPTS." + stag)

    return


def savebool(fptr, bval, stag):

    if (isinstance(bval, bool)):
        if (bval is True):
            fptr.write("  " + stag + "=TRUE \n")
        else:
            fptr.write("  " + stag + "=FALSE\n")
    else:
        raise TypeError(
            "Invalid [BOOLS] data: OPTS." + stag)

    return


def saveprj(name, opts):
    """
    SAVEPRJ: save a PRJ config. obj. to file.

    SAVEPRJ(NAME, OPTS)

    OPTS is a user-defined set of projection data. See PRJ_t
    for details.

    Data in OPTS is written as-needed -- any objects defined
    will be saved to file.

    """

    if (not isinstance(name, str)):
        raise TypeError("Incorrect type: NAME.")

    if (not isinstance(opts, jigsaw_prj_t)):
        raise TypeError("Incorrect type: OPTS.")

    fext = Path(name).suffix

    if (fext.strip() != ".prj"): name = name + ".prj"

    with Path(name).open("w") as fptr:

        fptr.write(
            "# " + Path(name).name +
            " config. file;"
            " created by JIGSAW's PYTHON interface \n")

    #------------------------------------------ MISC options
        if (opts.prjID is not None):
            savechar(fptr, opts.prjID, "PRJID")

        if (opts.radii is not None):
            savereal(fptr, opts.radii, "RADII")

        if (opts.xbase is not None):
            savereal(fptr, opts.xbase, "X-MID")

        if (opts.ybase is not None):
            savereal(fptr, opts.ybase, "Y-MID")

    return

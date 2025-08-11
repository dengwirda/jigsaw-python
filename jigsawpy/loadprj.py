
from pathlib import Path
from jigsawpy.prj_t import jigsaw_prj_t


def loadprj(name, opts):
    """
    LOADPRJ: load a PRJ config. obj. from file.

    LOADPRJ(NAME, OPTS)

    OPTS is a user-defined set of projection data. See PRJ_t
    for details.

    Data in OPTS is loaded on-demand -- any objects included
    in the file will be read.

    """

    if (not isinstance(name, str)):
        raise TypeError("Incorrect type: NAME.")

    if (not isinstance(opts, jigsaw_prj_t)):
        raise TypeError("Incorrect type: OPTS.")

    with Path(name).open("r") as fptr:
        while (True):

        #----------------------- get the next line from file
            line = fptr.readline()

            if (len(line) != +0):

        #----------------------- parse next non-null section
                line = line.strip()
                if (line[0] == "#"): continue

                ltag = line.split("=")
                item = ltag[0].upper().strip()

        #-------------------------------------- PROJ options
                if (item == "PRJID"):
                    opts.prjID = ltag[1].strip()

                if (item == "RADII"):
                    opts.radii = float(ltag[1])

                if (item == "X-MID"):
                    opts.xbase = float(ltag[1])

                if (item == "Y-MID"):
                    opts.ybase = float(ltag[1])

            else:
        #----------------------- reached end-of-file: done!!
                break

    return

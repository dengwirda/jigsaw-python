
from pathlib import Path
from jigsawpy.jig_t import jigsaw_jig_t


def loadjig(name, opts):
    """
    LOADJIG: load a JIG config. obj. from file.

    LOADJIG(NAME, OPTS)

    OPTS is a user-defined set of meshing options. See JIG_t
    for details.

    Data in OPTS is loaded on-demand -- any objects included
    in the file will be read.

    """

    if (not isinstance(name, str)):
        raise Exception("Incorrect type: NAME.")

    if (not isinstance(opts, jigsaw_jig_t)):
        raise Exception("Incorrect type: OPTS.")

    with Path(name).open("r") as fptr:
        while (True):

        #----------------------- get the next line from file
            line = fptr.readline()

            if (len(line) != +0):

        #----------------------- parse next non-null section
                if (line[0] == " "):
                    continue

                ltag = line.split("=")
                item = ltag[0].upper().strip()

        #-------------------------------------- MISC options
                if (item == "VERBOSITY"):
                    opts.verbosity = int(ltag[1])

                if (item == "TRIA_FILE"):
                    opts.tria_file = ltag[1].strip()

                if (item == "BNDS_FILE"):
                    opts.bnds_file = ltag[1].strip()

        #-------------------------------------- INIT options
                if (item == "INIT_FILE"):
                    opts.init_file = ltag[1].strip()

                if (item == "INIT_NEAR"):
                    opts.init_near = float(ltag[1])

        #-------------------------------------- GEOM options
                if (item == "GEOM_FILE"):
                    opts.geom_file = ltag[1].strip()

                if (item == "GEOM_SEED"):
                    opts.geom_seed = int(ltag[1])

                if (item == "GEOM_FEAT"):
                    opts.geom_feat = bool(ltag[1])

                if (item == "GEOM_PHI1"):
                    opts.geom_phi1 = float(ltag[1])
                if (item == "GEOM_PHI2"):
                    opts.geom_phi2 = float(ltag[1])

                if (item == "GEOM_ETA1"):
                    opts.geom_eta1 = float(ltag[1])
                if (item == "GEOM_ETA2"):
                    opts.geom_eta2 = float(ltag[1])

        #-------------------------------------- HFUN options
                if (item == "HFUN_FILE"):
                    opts.hfun_file = ltag[1].strip()

                if (item == "HFUN_SCAL"):
                    opts.hfun_scal = ltag[1].strip()

                if (item == "HFUN_HMAX"):
                    opts.hfun_hmax = float(ltag[1])
                if (item == "HFUN_HMIN"):
                    opts.hfun_hmin = float(ltag[1])

        #-------------------------------------- MESH options
                if (item == "MESH_FILE"):
                    opts.mesh_file = ltag[1].strip()

                if (item == "MESH_KERN"):
                    opts.mesh_kern = ltag[1].strip()
                if (item == "BNDS_KERN"):
                    opts.bnds_kern = ltag[1].strip()

                if (item == "MESH_ITER"):
                    opts.mesh_iter = int(ltag[1])

                if (item == "MESH_DIMS"):
                    opts.mesh_dims = int(ltag[1])

                if (item == "MESH_TOP1"):
                    opts.mesh_top1 = bool(ltag[1])
                if (item == "MESH_TOP2"):
                    opts.mesh_top2 = bool(ltag[1])

                if (item == "MESH_SIZ1"):
                    opts.mesh_siz1 = float(ltag[1])
                if (item == "MESH_SIZ2"):
                    opts.mesh_siz2 = float(ltag[1])
                if (item == "MESH_SIZ3"):
                    opts.mesh_siz3 = float(ltag[1])

                if (item == "MESH_EPS1"):
                    opts.mesh_eps1 = float(ltag[1])
                if (item == "MESH_EPS2"):
                    opts.mesh_eps2 = float(ltag[1])

                if (item == "MESH_RAD2"):
                    opts.mesh_rad2 = float(ltag[1])
                if (item == "MESH_RAD3"):
                    opts.mesh_rad3 = float(ltag[1])

                if (item == "MESH_OFF2"):
                    opts.mesh_off2 = float(ltag[1])
                if (item == "MESH_OFF3"):
                    opts.mesh_off3 = float(ltag[1])

                if (item == "MESH_SNK2"):
                    opts.mesh_snk2 = float(ltag[1])
                if (item == "MESH_SNK3"):
                    opts.mesh_snk3 = float(ltag[1])

                if (item == "MESH_VOL3"):
                    opts.mesh_vol3 = float(ltag[1])

        #-------------------------------------- OPTM options
                if (item == "OPTM_KERN"):
                    opts.optm_kern = ltag[1].strip()

                if (item == "OPTM_ITER"):
                    opts.optm_iter = int(ltag[1])

                if (item == "OPTM_QTOL"):
                    opts.optm_qtol = float(ltag[1])
                if (item == "OPTM_QLIM"):
                    opts.optm_qlim = float(ltag[1])

                if (item == "OPTM_ZIP_"):
                    opts.optm_zip_ = bool(ltag[1])
                if (item == "OPTM_DIV_"):
                    opts.optm_div_ = bool(ltag[1])
                if (item == "OPTM_TRIA"):
                    opts.optm_tria = bool(ltag[1])
                if (item == "OPTM_DUAL"):
                    opts.optm_dual = bool(ltag[1])

            else:
        #----------------------- reached end-of-file: done!!
                break

    return




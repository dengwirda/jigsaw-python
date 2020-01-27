
from pathlib import Path
from jigsawpy.jig_t import jigsaw_jig_t


def savechar(fptr, sval, stag):

    if (isinstance(sval, str)):
        fptr.write("  " + stag + "=" + sval + "\n")
    else:
        raise Exception(
            "Invalid [CHARA] data: OPTS." + stag)

    return


def saveints(fptr, ival, stag):

    if (isinstance(ival, int)):
        fptr.write(
            "  " + stag + "=" + str(ival) + "\n")
    else:
        raise Exception(
            "Invalid [INDEX] data: OPTS." + stag)

    return


def savereal(fptr, fval, stag):

    if (isinstance(fval, float)):
        fptr.write(
            "  " + stag + "=" + str(fval) + "\n")
    else:
        raise Exception(
            "Invalid [FLOAT] data: OPTS." + stag)

    return


def savebool(fptr, bval, stag):

    if (isinstance(bval, bool)):
        if (bval is True):
            fptr.write("  " + stag + "=TRUE \n")
        else:
            fptr.write("  " + stag + "=FALSE\n")
    else:
        raise Exception(
            "Invalid [BOOLS] data: OPTS." + stag)

    return


def savejig(name, opts):
    """
    SAVEJIG: save a JIG config. obj. to file.

    SAVEJIG(NAME, OPTS)

    OPTS is a user-defined set of meshing options. See JIG_t
    for details.

    Data in OPTS is written as-needed -- any objects defined
    will be saved to file.

    """

    if (not isinstance(name, str)):
        raise Exception("Incorrect type: NAME.")

    if (not isinstance(opts, jigsaw_jig_t)):
        raise Exception("Incorrect type: OPTS.")

    fext = Path(name).suffix

    if (fext.strip() != ".jig"): name = name + ".jig"

    with Path(name).open("w") as fptr:

        fptr.write("# " + Path(name).name +
            " config. file;"
            " created by JIGSAW's PYTHON interface \n")

    #------------------------------------------ MISC options
        if (opts.verbosity is not None):
            saveints(fptr, opts.verbosity, "VERBOSITY")

        if (opts.tria_file is not None):
            savechar(fptr, opts.tria_file, "TRIA_FILE")
        if (opts.bnds_file is not None):
            savechar(fptr, opts.bnds_file, "BNDS_FILE")

    #------------------------------------------ INIT options
        if (opts.init_file is not None):
            savechar(fptr, opts.init_file, "INIT_FILE")

        if (opts.init_near is not None):
            savereal(fptr, opts.init_near, "INIT_NEAR")

    #------------------------------------------ GEOM options
        if (opts.geom_file is not None):
            savechar(fptr, opts.geom_file, "GEOM_FILE")

        if (opts.geom_seed is not None):
            saveints(fptr, opts.geom_seed, "GEOM_SEED")

        if (opts.geom_feat is not None):
            savebool(fptr, opts.geom_feat, "GEOM_FEAT")

        if (opts.geom_phi1 is not None):
            savereal(fptr, opts.geom_phi1, "GEOM_PHI1")
        if (opts.geom_phi2 is not None):
            savereal(fptr, opts.geom_phi2, "GEOM_PHI2")

        if (opts.geom_eta1 is not None):
            savereal(fptr, opts.geom_eta1, "GEOM_ETA1")
        if (opts.geom_eta2 is not None):
            savereal(fptr, opts.geom_eta2, "GEOM_ETA2")

    #------------------------------------------ HFUN options
        if (opts.hfun_file is not None):
            savechar(fptr, opts.hfun_file, "HFUN_FILE")

        if (opts.hfun_scal is not None):
            savechar(fptr, opts.hfun_scal, "HFUN_SCAL")

        if (opts.hfun_hmax is not None):
            savereal(fptr, opts.hfun_hmax, "HFUN_HMAX")
        if (opts.hfun_hmin is not None):
            savereal(fptr, opts.hfun_hmin, "HFUN_HMIN")

    #------------------------------------------ MESH options
        if (opts.mesh_file is not None):
            savechar(fptr, opts.mesh_file, "MESH_FILE")

        if (opts.mesh_kern is not None):
            savechar(fptr, opts.mesh_kern, "MESH_KERN")
        if (opts.bnds_kern is not None):
            savechar(fptr, opts.bnds_kern, "BNDS_KERN")

        if (opts.mesh_iter is not None):
            saveints(fptr, opts.mesh_iter, "MESH_ITER")

        if (opts.mesh_dims is not None):
            saveints(fptr, opts.mesh_dims, "MESH_DIMS")

        if (opts.mesh_top1 is not None):
            savebool(fptr, opts.mesh_top1, "MESH_TOP1")
        if (opts.mesh_top2 is not None):
            savebool(fptr, opts.mesh_top2, "MESH_TOP2")

        if (opts.mesh_siz1 is not None):
            savereal(fptr, opts.mesh_siz1, "MESH_SIZ1")
        if (opts.mesh_siz2 is not None):
            savereal(fptr, opts.mesh_siz2, "MESH_SIZ2")
        if (opts.mesh_siz3 is not None):
            savereal(fptr, opts.mesh_siz3, "MESH_SIZ3")

        if (opts.mesh_eps1 is not None):
            savereal(fptr, opts.mesh_eps1, "MESH_EPS1")
        if (opts.mesh_eps2 is not None):
            savereal(fptr, opts.mesh_eps2, "MESH_EPS2")

        if (opts.mesh_rad2 is not None):
            savereal(fptr, opts.mesh_rad2, "MESH_RAD2")
        if (opts.mesh_rad3 is not None):
            savereal(fptr, opts.mesh_rad3, "MESH_RAD3")

        if (opts.mesh_off2 is not None):
            savereal(fptr, opts.mesh_off2, "MESH_OFF2")
        if (opts.mesh_off3 is not None):
            savereal(fptr, opts.mesh_off3, "MESH_OFF3")

        if (opts.mesh_snk2 is not None):
            savereal(fptr, opts.mesh_snk2, "MESH_SNK2")
        if (opts.mesh_snk3 is not None):
            savereal(fptr, opts.mesh_snk3, "MESH_SNK3")

        if (opts.mesh_vol3 is not None):
            savereal(fptr, opts.mesh_vol3, "MESH_VOL3")

    #------------------------------------------ OPTM options
        if (opts.optm_kern is not None):
            savechar(fptr, opts.optm_kern, "OPTM_KERN")

        if (opts.optm_iter is not None):
            saveints(fptr, opts.optm_iter, "OPTM_ITER")

        if (opts.optm_qtol is not None):
            savereal(fptr, opts.optm_qtol, "OPTM_QTOL")
        if (opts.optm_qlim is not None):
            savereal(fptr, opts.optm_qlim, "OPTM_QLIM")

        if (opts.optm_zip_ is not None):
            savebool(fptr, opts.optm_zip_, "OPTM_ZIP_")
        if (opts.optm_div_ is not None):
            savebool(fptr, opts.optm_div_, "OPTM_DIV_")
        if (opts.optm_tria is not None):
            savebool(fptr, opts.optm_tria, "OPTM_TRIA")
        if (opts.optm_dual is not None):
            savebool(fptr, opts.optm_dual, "OPTM_DUAL")

    return




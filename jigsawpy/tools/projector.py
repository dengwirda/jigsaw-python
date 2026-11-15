
import numpy as np


def stereo3_f(rrad, xpos, ypos, xmid, ymid):
    """
    STEREO3_f: compute the forward stereographic projection.

    """

    #------------------------------------ do forward mapping

    ccxd = np.cos(xpos - xmid)

    ccym = np.cos(ymid)
    ccyp = np.cos(ypos)

    ssxd = np.sin(xpos - xmid)

    ssym = np.sin(ymid)
    ssyp = np.sin(ypos)

    kden = \
        +1.0 + ssym * ssyp + ccym * ccyp * ccxd

    kval = +2.0 * rrad / kden ** 1

    dval = -2.0 * rrad / kden ** 2

    xnew = \
        kval * ccyp * ssxd
    ynew = \
        kval * ccym * ssyp - \
        kval * ssym * ccyp * ccxd

    #------------------------------------ compute indicatrix

    dkdy = \
        dval * ssym * ccyp - \
        dval * ccym * ssyp * ccxd

    dxdy = \
        dkdy * ccyp * ssxd - kval * ssyp * ssxd

    dydy = \
        dkdy * ccym * ssyp - \
        dkdy * ssym * ccyp * ccxd + \
        kval * ccym * ccyp + \
        kval * ssym * ssyp * ccxd

    scal = \
        +1.0 / rrad * np.sqrt(dxdy**2 + dydy**2)

    return xnew, ynew, scal


def stereo3_i(rrad, xpos, ypos, xmid, ymid):
    """
    STEREO3_i: compute the inverse stereographic projection.

    """

    #------------------------------------ do inverse mapping

    rval = np.hypot(xpos, ypos)
    zero = (rval == 0.)

    cval = +2.0 * np.arctan2(rval, +2.0 * rrad)

    ccym = np.cos(ymid)
    cccv = np.cos(cval)

    ssym = np.sin(ymid)
    sscv = np.sin(cval)

    xtmp = rval * ccym * cccv - ypos * ssym * sscv

    xnew = xmid + np.arctan2(xpos * sscv, xtmp)
    xnew = np.where(zero, xmid, xnew)

    ytmp = ypos * ccym * sscv

    rlim = np.where(zero, +1.0, rval)
    ynew = np.arcsin(cccv * ssym + ytmp / rlim)
    ynew = np.where(zero, ymid, ynew)

    #------------------------------------ compute indicatrix

    ccxd = np.cos(xnew - xmid)
    ssxd = np.sin(xnew - xmid)

    ccyn = np.cos(ynew)
    ssyn = np.sin(ynew)

    kden = \
        +1.0 + ssym * ssyn + ccym * ccyn * ccxd

    dval = -2.0 * rrad / kden ** 2

    kval = +2.0 * rrad / kden ** 1

    dkdy = \
        dval * ssym * ccyn - \
        dval * ccym * ssyn * ccxd

    dxdy = \
        dkdy * ccyn * ssxd - kval * ssyn * ssxd

    dydy = \
        dkdy * ccym * ssyn - \
        dkdy * ssym * ccyn * ccxd + \
        kval * ccym * ccyn + \
        kval * ssym * ssyn * ccxd

    scal = \
        rrad * +1.0 / np.sqrt(dxdy**2 + dydy**2)
    scal = np.where(zero, 1., scal)

    return xnew, ynew, scal


def stereo3(rrad, xpos, ypos, xmid, ymid, kind):
    """
    STEREO3: calculate a "rotated" stereographic projection.

    XNEW,YNEW,SCAL = STEREO3(RRAD,XPOS,YPOS,XMID,YMID,KIND)
    returns the stereographic projection [XNEW,YNEW] of the
    lon-lat points [RRAD,XPOS,YPOS], where RRAD is the
    radius of the sphere, and [XPOS,YPOS] are arrays of lon-
    gitude and latitude, respectively. Angles are measured
    in radians. [XMID,YMID] are the lon-lat coordinates that
    the mapping is 'centred' about. The stereographic proje-
    ction is a conformal mapping; preserving angles.

    XNEW,YNEW,SCAL = STEREO3(..., KIND) specifies the direc-
    tion of the mapping. KIND = "FWD" defines a forward map-
    ping, and KIND = "INV" defines an inverse mapping. Here,
    the role of [XNEW,YNEW] and [XPOS,YPOS] are exchanged,
    with [XPOS,YPOS] the stereographic coordinates, and
    [XNEW,YNEW] the resulting lon-lat spherical angles.

    SCAL is the local length scale-factor for the requested
    mapping: plane length / sphere length for "FWD", and its
    reciprocal for "INV", at each corresponding point.

    """

    if   (kind.lower() == "fwd"):

        xnew, ynew, scal = \
            stereo3_f(rrad, xpos, ypos, xmid, ymid)

    elif (kind.lower() == "inv"):

        xnew, ynew, scal = \
            stereo3_i(rrad, xpos, ypos, xmid, ymid)

    return xnew, ynew, scal

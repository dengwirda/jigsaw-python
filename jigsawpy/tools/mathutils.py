
import numpy as np


def S2toR3(radii, S2):

# S2toR3: convert from spheroidal into cartesian coordinates

    E3 = np.empty(
        (S2.shape[0], 3), dtype=S2.dtype)

    C0 = np.cos(S2[:, 0])
    C1 = np.cos(S2[:, 1])

    S0 = np.sin(S2[:, 0])
    S1 = np.sin(S2[:, 1])

    E3[:, 0] = radii[0] * C0 * C1
    E3[:, 1] = radii[1] * S0 * C1

    E3[:, 2] = radii[2] * S1

    return E3


def R3toS2(radii, E3):

# R3toS2: convert from cartesian into spheroidal coordinates

    S2 = np.empty(
        (E3.shape[0], 2), dtype=E3.dtype)

    xm = E3[:, 0] * radii[1]
    ym = E3[:, 1] * radii[0]
    zr = E3[:, 2] / radii[2]

    zr = np.maximum(np.minimum(zr, +1.), -1.)

    S2[:, 1] = np.arcsin(zr)
    S2[:, 0] = np.arctan2(ym, xm)

    return S2


def det_2x2(amat):

# DET-2x2: compute determinants for a set of 2 x 2 matrices.

    return \
        amat[0, 0, :] * amat[1, 1, :] - \
        amat[0, 1, :] * amat[1, 0, :]


def det_3x3(amat):

# DET-3x3: compute determinants for a set of 3 x 3 matrices.

    detA = \
        amat[1, 1, :] * amat[2, 2, :] - \
        amat[1, 2, :] * amat[2, 1, :]

    detB = \
        amat[1, 0, :] * amat[2, 2, :] - \
        amat[1, 2, :] * amat[2, 0, :]

    detC = \
        amat[1, 0, :] * amat[2, 1, :] - \
        amat[1, 1, :] * amat[2, 0, :]

    return \
        amat[0, 0, :] * detA - \
        amat[0, 1, :] * detB + \
        amat[0, 2, :] * detC


def inv_2x2(amat):

# INV-2x2: calculate inverse(s) for a set of 2 x 2 matrices.

    adet = det_2x2(amat)

    ainv = np.empty((2, 2, amat.shape[2]))

    ainv[0, 0, :] = +amat[1, 1, :]
    ainv[1, 1, :] = +amat[0, 0, :]
    ainv[0, 1, :] = -amat[0, 1, :]
    ainv[1, 0, :] = -amat[1, 0, :]

    return ainv, adet


def inv_3x3(amat):

# INV-3x3: calculate inverse(s) for a set of 3 x 3 matrices.

    adet = det_3x3(amat)

    ainv = np.empty((3, 3, amat.shape[2]))

    ainv[0, 0, :] = \
        amat[2, 2, :] * amat[1, 1, :] - \
        amat[2, 1, :] * amat[1, 2, :]

    ainv[0, 1, :] = \
        amat[2, 1, :] * amat[0, 2, :] - \
        amat[2, 2, :] * amat[0, 1, :]

    ainv[0, 2, :] = \
        amat[1, 2, :] * amat[0, 1, :] - \
        amat[1, 1, :] * amat[0, 2, :]

    ainv[1, 0, :] = \
        amat[2, 0, :] * amat[1, 2, :] - \
        amat[2, 2, :] * amat[1, 0, :]

    ainv[1, 1, :] = \
        amat[2, 2, :] * amat[0, 0, :] - \
        amat[2, 0, :] * amat[0, 2, :]

    ainv[1, 2, :] = \
        amat[1, 0, :] * amat[0, 2, :] - \
        amat[1, 2, :] * amat[0, 0, :]

    ainv[2, 0, :] = \
        amat[2, 1, :] * amat[1, 0, :] - \
        amat[2, 0, :] * amat[1, 1, :]

    ainv[2, 1, :] = \
        amat[2, 0, :] * amat[0, 1, :] - \
        amat[2, 1, :] * amat[0, 0, :]

    ainv[2, 2, :] = \
        amat[1, 1, :] * amat[0, 0, :] - \
        amat[1, 0, :] * amat[0, 1, :]

    return ainv, adet

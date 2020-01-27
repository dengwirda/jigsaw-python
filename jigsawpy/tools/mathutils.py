
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




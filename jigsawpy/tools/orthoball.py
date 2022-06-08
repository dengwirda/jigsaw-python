
import numpy as np
from jigsawpy.tools.predicate import istri_1, istri_2, istri_3
from jigsawpy.tools.mathutils import inv_2x2, inv_3x3


def tribal1(ppos, tri1):
    """
    TRIBAL1 compute the circumballs associated with a 1-cell
    triangulation embedded in R^2 or R^3.

    BALL = TRIBAL1(PPOS,TRI1) returns the set of circumballs
    associated with the cells in [PPOS,TRI1], such that
    BALL = [PMID,RRAD**2].

    """

    return pwrbal1(
        ppos, np.zeros((ppos.shape[0], 1)), tri1)


def tribal2(ppos, tri2):
    """
    TRIBAL2 compute the circumballs associated with a 2-cell
    triangulation embedded in R^2 or R^3.

    BALL = TRIBAL2(PPOS,TRI2) returns the set of circumballs
    associated with the cells in [PPOS,TRI2], such that
    BALL = [PMID,RRAD**2].

    """

    return pwrbal2(
        ppos, np.zeros((ppos.shape[0], 1)), tri2)


def tribal3(ppos, tri3):
    """
    TRIBAL3 compute the circumballs associated with a 3-cell
    triangulation embedded in R^3.

    BALL = TRIBAL3(PPOS,TRI3) returns the set of circumballs
    associated with the cells in [PPOS,TRI3], such that
    BALL = [PMID,RRAD**2].

    """

    return pwrbal3(
        ppos, np.zeros((ppos.shape[0], 1)), tri3)


def pwrbal1(ppos, ppwr, tri1):
    """
    PWRBAL1 compute the ortho-balls associated with a 1-cell
    triangulation embedded in R^2 or R^3.

    BALL = PWRBAL1(PPOS,PPWR,TRI1) returns the set of power
    balls associated with the cells in [PPOS,TRI1], such
    that BALL = [PMID,RRAD**2]. PPWR is the vector of power
    values associated with the input vertices PPOS.

    """

    okay = istri_1(ppos, tri1)

    if   (ppos.shape[1] == 2):
    #-------------------------------------------- lin offset
        ppwr = np.reshape(ppwr, (ppos.shape[0], 1))

        pp12 = \
            ppos[tri1[:, 0], :] - \
            ppos[tri1[:, 1], :]

        ww12 = ppwr[tri1[:, 0]] - ppwr[tri1[:, 1]]

        dp12 = np.sum(
            pp12 ** 2, axis=1, keepdims=True)

        tpwr = 0.5 * (ww12 + dp12) / dp12

        ball = np.zeros((tri1.shape[0], 3))
        ball[:, 0:2] = \
            ppos[tri1[:, 0], :] - tpwr * pp12

    #-------------------------------------------- mean radii
        vrad = ball[:, 0:2] - ppos[tri1[:, 0], :]
        rad1 = np.sum(
            vrad ** 2, axis=1, keepdims=True)

        vrad = ball[:, 0:2] - ppos[tri1[:, 1], :]
        rad2 = np.sum(
            vrad ** 2, axis=1, keepdims=True)

        rad1 = rad1 - ppwr[tri1[:, 0]]
        rad2 = rad2 - ppwr[tri1[:, 1]]

        ball[:, 2] = \
            np.squeeze((rad1 + rad2) / +2.00)

    elif (ppos.shape[1] == 3):
    #-------------------------------------------- lin offset
        ppwr = np.reshape(ppwr, (ppos.shape[0], 1))

        pp12 = \
            ppos[tri1[:, 0], :] - \
            ppos[tri1[:, 1], :]

        ww12 = ppwr[tri1[:, 0]] - ppwr[tri1[:, 1]]

        dp12 = np.sum(
            pp12 ** 2, axis=1, keepdims=True)

        tpwr = 0.5 * (ww12 + dp12) / dp12

        ball = np.zeros((tri1.shape[0], 4))
        ball[:, 0:3] = \
            ppos[tri1[:, 0], :] - tpwr * pp12

    #-------------------------------------------- mean radii
        vrad = ball[:, 0:3] - ppos[tri1[:, 0], :]
        rad1 = np.sum(
            vrad ** 2, axis=1, keepdims=True)

        vrad = ball[:, 0:3] - ppos[tri1[:, 1], :]
        rad2 = np.sum(
            vrad ** 2, axis=1, keepdims=True)

        rad1 = rad1 - ppwr[tri1[:, 0]]
        rad2 = rad2 - ppwr[tri1[:, 1]]

        ball[:, 3] = \
            np.squeeze((rad1 + rad2) / +2.00)

    else:
        raise ValueError("Unsupported dimension.")

    return ball


def pwrbal2(ppos, ppwr, tri2):
    """
    PWRBAL2 compute the ortho-balls associated with a 2-cell
    triangulation embedded in R^2 or R^3.

    BALL = PWRBAL2(PPOS,PPWR,TRI2) returns the set of power
    balls associated with the cells in [PPOS,TRI2], such
    that BALL = [PMID,RRAD**2]. PPWR is the vector of power
    values associated with the input vertices PPOS.

    """

    okay = istri_2(ppos, tri2)

    if   (ppos.shape[1] == 2):
    #-------------------------------------------- alloc work
        amat = np.zeros((2, 2, tri2.shape[0]))
        vrhs = np.zeros((2, 1, tri2.shape[0]))
        ball = np.zeros((tri2.shape[0], 3))

        ppwr = np.reshape(ppwr, (ppos.shape[0], 1))

    #-------------------------------------------- lhs matrix
        ab = ppos[tri2[:, 1], :] - ppos[tri2[:, 0], :]
        ac = ppos[tri2[:, 2], :] - ppos[tri2[:, 0], :]

        amat[0, 0, :] = ab[:, 0] * +2.0
        amat[0, 1, :] = ab[:, 1] * +2.0

        amat[1, 0, :] = ac[:, 0] * +2.0
        amat[1, 1, :] = ac[:, 1] * +2.0

    #-------------------------------------------- rhs vector
        vrhs[0, 0, :] = np.squeeze(
            np.sum(ab * ab, axis=1, keepdims=True) -
            (ppwr[tri2[:, 1]] - ppwr[tri2[:, 0]]))

        vrhs[1, 0, :] = np.squeeze(
            np.sum(ac * ac, axis=1, keepdims=True) -
            (ppwr[tri2[:, 2]] - ppwr[tri2[:, 0]]))

    #-------------------------------------------- solve sys.
        imat, adet = inv_2x2(amat)

        ball[:, 0] = (
            imat[0, 0, :] * vrhs[0, 0, :] +
            imat[0, 1, :] * vrhs[1, 0, :])

        ball[:, 1] = (
            imat[1, 0, :] * vrhs[0, 0, :] +
            imat[1, 1, :] * vrhs[1, 0, :])

        ball[:, 0] = ball[:, 0] / adet
        ball[:, 1] = ball[:, 1] / adet

        ball[:, 0:2] = \
            ppos[tri2[:, 0], :] + ball[:, 0:2]

    #-------------------------------------------- mean radii
        vrad = ball[:, 0:2] - ppos[tri2[:, 0], :]
        rad1 = np.sum(
            vrad ** 2, axis=1, keepdims=True)

        vrad = ball[:, 0:2] - ppos[tri2[:, 1], :]
        rad2 = np.sum(
            vrad ** 2, axis=1, keepdims=True)

        vrad = ball[:, 0:2] - ppos[tri2[:, 2], :]
        rad3 = np.sum(
            vrad ** 2, axis=1, keepdims=True)

        rad1 = rad1 - ppwr[tri2[:, 0]]
        rad2 = rad2 - ppwr[tri2[:, 1]]
        rad3 = rad3 - ppwr[tri2[:, 2]]

        ball[:, 2] = np.squeeze(
            (rad1 + rad2 + rad3) / +3.0
        )

    elif (ppos.shape[1] == 3):
    #-------------------------------------------- alloc work
        amat = np.zeros((3, 3, tri2.shape[0]))
        vrhs = np.zeros((3, 1, tri2.shape[0]))
        ball = np.zeros((tri2.shape[0], 4))

        ppwr = np.reshape(ppwr, (ppos.shape[0], 1))

    #-------------------------------------------- lhs matrix
        ab = ppos[tri2[:, 1], :] - ppos[tri2[:, 0], :]
        ac = ppos[tri2[:, 2], :] - ppos[tri2[:, 0], :]

        amat[0, 0, :] = ab[:, 0] * +2.0
        amat[0, 1, :] = ab[:, 1] * +2.0
        amat[0, 2, :] = ab[:, 2] * +2.0

        amat[1, 0, :] = ac[:, 0] * +2.0
        amat[1, 1, :] = ac[:, 1] * +2.0
        amat[1, 2, :] = ac[:, 2] * +2.0

        nv = np.cross(ab, ac)

        amat[2, 0, :] = nv[:, 0] * +1.0
        amat[2, 1, :] = nv[:, 1] * +1.0
        amat[2, 2, :] = nv[:, 2] * +1.0

    #-------------------------------------------- rhs vector
        vrhs[0, 0, :] = np.squeeze(
            np.sum(ab * ab, axis=1, keepdims=True) -
            (ppwr[tri2[:, 1]] - ppwr[tri2[:, 0]]))

        vrhs[1, 0, :] = np.squeeze(
            np.sum(ac * ac, axis=1, keepdims=True) -
            (ppwr[tri2[:, 2]] - ppwr[tri2[:, 0]]))

    #-------------------------------------------- solve sys.
        imat, adet = inv_3x3(amat)

        ball[:, 0] = (
            imat[0, 0, :] * vrhs[0, 0, :] +
            imat[0, 1, :] * vrhs[1, 0, :] +
            imat[0, 2, :] * vrhs[2, 0, :])

        ball[:, 1] = (
            imat[1, 0, :] * vrhs[0, 0, :] +
            imat[1, 1, :] * vrhs[1, 0, :] +
            imat[1, 2, :] * vrhs[2, 0, :])

        ball[:, 2] = (
            imat[2, 0, :] * vrhs[0, 0, :] +
            imat[2, 1, :] * vrhs[1, 0, :] +
            imat[2, 2, :] * vrhs[2, 0, :])

        ball[:, 0] = ball[:, 0] / adet
        ball[:, 1] = ball[:, 1] / adet
        ball[:, 2] = ball[:, 2] / adet

        ball[:, 0:3] = \
            ppos[tri2[:, 0], :] + ball[:, 0:3]

    #-------------------------------------------- mean radii
        vrad = ball[:, 0:3] - ppos[tri2[:, 0], :]
        rad1 = np.sum(
            vrad ** 2, axis=1, keepdims=True)

        vrad = ball[:, 0:3] - ppos[tri2[:, 1], :]
        rad2 = np.sum(
            vrad ** 2, axis=1, keepdims=True)

        vrad = ball[:, 0:3] - ppos[tri2[:, 2], :]
        rad3 = np.sum(
            vrad ** 2, axis=1, keepdims=True)

        rad1 = rad1 - ppwr[tri2[:, 0]]
        rad2 = rad2 - ppwr[tri2[:, 1]]
        rad3 = rad3 - ppwr[tri2[:, 2]]

        ball[:, 3] = np.squeeze(
            (rad1 + rad2 + rad3) / +3.0
        )

    else:
        raise ValueError("Unsupported dimension.")

    return ball


def pwrbal3(ppos, ppwr, tri3):
    """
    PWRBAL3 compute the ortho-balls associated with a 3-cell
    triangulation embedded in R^3.

    BALL = PWRBAL3(PPOS,PPWR,TRI3) returns the set of power
    balls associated with the cells in [PPOS,TRI3], such
    that BALL = [PMID,RRAD**2]. PPWR is the vector of power
    values associated with the input vertices PPOS.

    """

    okay = istri_3(ppos, tri3)

    if (ppos.shape[1] == 3):
    #-------------------------------------------- alloc work
        amat = np.zeros((3, 3, tri3.shape[0]))
        vrhs = np.zeros((3, 1, tri3.shape[0]))
        ball = np.zeros((tri3.shape[0], 4))

        ppwr = np.reshape(ppwr, (ppos.shape[0], 1))

    #-------------------------------------------- lhs matrix
        ab = ppos[tri3[:, 1], :] - ppos[tri3[:, 0], :]
        ac = ppos[tri3[:, 2], :] - ppos[tri3[:, 0], :]
        ad = ppos[tri3[:, 3], :] - ppos[tri3[:, 0], :]

        amat[0, 0, :] = ab[:, 0] * +2.0
        amat[0, 1, :] = ab[:, 1] * +2.0
        amat[0, 2, :] = ab[:, 2] * +2.0

        amat[1, 0, :] = ac[:, 0] * +2.0
        amat[1, 1, :] = ac[:, 1] * +2.0
        amat[1, 2, :] = ac[:, 2] * +2.0

        amat[2, 0, :] = ad[:, 0] * +2.0
        amat[2, 1, :] = ad[:, 1] * +2.0
        amat[2, 2, :] = ad[:, 2] * +2.0

    #-------------------------------------------- rhs vector
        vrhs[0, 0, :] = np.squeeze(
            np.sum(ab * ab, axis=1, keepdims=True) -
            (ppwr[tri3[:, 1]] - ppwr[tri3[:, 0]]))

        vrhs[1, 0, :] = np.squeeze(
            np.sum(ac * ac, axis=1, keepdims=True) -
            (ppwr[tri3[:, 2]] - ppwr[tri3[:, 0]]))

        vrhs[2, 0, :] = np.squeeze(
            np.sum(ad * ad, axis=1, keepdims=True) -
            (ppwr[tri3[:, 3]] - ppwr[tri3[:, 0]]))

    #-------------------------------------------- solve sys.
        imat, adet = inv_3x3(amat)

        ball[:, 0] = (
            imat[0, 0, :] * vrhs[0, 0, :] +
            imat[0, 1, :] * vrhs[1, 0, :] +
            imat[0, 2, :] * vrhs[2, 0, :])

        ball[:, 1] = (
            imat[1, 0, :] * vrhs[0, 0, :] +
            imat[1, 1, :] * vrhs[1, 0, :] +
            imat[1, 2, :] * vrhs[2, 0, :])

        ball[:, 2] = (
            imat[2, 0, :] * vrhs[0, 0, :] +
            imat[2, 1, :] * vrhs[1, 0, :] +
            imat[2, 2, :] * vrhs[2, 0, :])

        ball[:, 0] = ball[:, 0] / adet
        ball[:, 1] = ball[:, 1] / adet
        ball[:, 2] = ball[:, 2] / adet

        ball[:, 0:3] = \
            ppos[tri3[:, 0], :] + ball[:, 0:3]

    #-------------------------------------------- mean radii
        vrad = ball[:, 0:3] - ppos[tri3[:, 0], :]
        rad1 = np.sum(
            vrad ** 2, axis=1, keepdims=True)

        vrad = ball[:, 0:3] - ppos[tri3[:, 1], :]
        rad2 = np.sum(
            vrad ** 2, axis=1, keepdims=True)

        vrad = ball[:, 0:3] - ppos[tri3[:, 2], :]
        rad3 = np.sum(
            vrad ** 2, axis=1, keepdims=True)

        vrad = ball[:, 0:3] - ppos[tri3[:, 3], :]
        rad4 = np.sum(
            vrad ** 2, axis=1, keepdims=True)

        rad1 = rad1 - ppwr[tri3[:, 0]]
        rad2 = rad2 - ppwr[tri3[:, 1]]
        rad3 = rad3 - ppwr[tri3[:, 2]]
        rad4 = rad4 - ppwr[tri3[:, 3]]

        ball[:, 3] = np.squeeze(
            (rad1 + rad2 + rad3 + rad4) / +4.0
        )

    else:
        raise ValueError("Unsupported dimension.")

    return ball

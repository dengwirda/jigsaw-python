r"""
------------------------------------------------------------
 *
 *   ,o, ,o,       /
 *    `   `  e88~88e  d88~\   /~~~8e Y88b    e    /
 *   888 888 88   88 C888         88b Y88b  d8b  /
 *   888 888 "8b_d8"  Y88b   e88~-888  Y888/Y88b/
 *   888 888  /        888D C88   888   Y8/  Y8/
 *   88P 888 Cb      \_88P   "8b_-888    Y    Y
 * \_8"       Y8""8D
 *
------------------------------------------------------------
 * JIGSAW: Interface to the JIGSAW meshing library.
------------------------------------------------------------
 *
 * Last updated: 04 Aug., 2025
 *
 * Copyright 2019-2025
 * Darren Engwirda
 * d.engwirda@gmail.com
 * https://github.com/dengwirda
 *
------------------------------------------------------------
 *
 * This program may be freely redistributed under the
 * condition that the copyright notices (including this
 * entire header) are not removed, and no compensation
 * is received through use of the software.  Private,
 * research, and institutional use is free.  You may
 * distribute modified versions of this code UNDER THE
 * CONDITION THAT THIS CODE AND ANY MODIFICATIONS MADE
 * TO IT IN THE SAME FILE REMAIN UNDER COPYRIGHT OF THE
 * ORIGINAL AUTHOR, BOTH SOURCE AND OBJECT CODE ARE
 * MADE FREELY AVAILABLE WITHOUT CHARGE, AND CLEAR
 * NOTICE IS GIVEN OF THE MODIFICATIONS.  Distribution
 * of this code as part of a commercial system is
 * permissible ONLY BY DIRECT ARRANGEMENT WITH THE
 * AUTHOR.  (If you are not directly supplying this
 * code to a customer, and you are instead telling them
 * how they can obtain it for free, then you are not
 * required to make any arrangement with me.)
 *
 * Disclaimer:  Neither I nor THE CONTRIBUTORS warrant
 * this code in any way whatsoever.  This code is
 * provided "as-is" to be used at your own risk.
 *
 * THE CONTRIBUTORS include:
 * (a) The University of Sydney
 * (b) The Massachusetts Institute of Technology
 * (c) Columbia University
 * (d) The National Aeronautics & Space Administration
 * (e) Los Alamos National Laboratory
 *
------------------------------------------------------------
 """

from jigsawpy.msh_t import jigsaw_msh_t
from jigsawpy.jig_t import jigsaw_jig_t
from jigsawpy.def_t import jigsaw_def_t
from jigsawpy.prj_t import jigsaw_prj_t

from jigsawpy import jigsaw, libsaw

from jigsawpy.loadmsh import loadmsh
from jigsawpy.savemsh import savemsh
from jigsawpy.loadjig import loadjig
from jigsawpy.savejig import savejig
from jigsawpy.loadprj import loadprj
from jigsawpy.saveprj import saveprj

from jigsawpy.certify import certify

from jigsawpy.project import project
from jigsawpy.bisect import bisect

from jigsawpy.tools.predicate import trivol2, trivol3, \
    normal1, normal2, orient1, orient2

from jigsawpy.tools.orthoball import tribal1, tribal2, \
    tribal3, pwrbal1, pwrbal2, pwrbal3

from jigsawpy.tools.scorecard import triscr2, triscr3, \
    trideg2, trideg3, triang2, triang3, \
    pwrscr2, pwrscr3, centre2, centre3

from jigsawpy.tools.projector import stereo3

from jigsawpy.tools.mathutils import R3toS2, S2toR3

from jigsawpy.tools.meshutils import attach, jumble

from jigsawpy.parse.saveoff import saveoff
from jigsawpy.parse.savewav import savewav
from jigsawpy.parse.savevtk import savevtk


class cmd:
#--------------------------------- expose cmd-line interface
    @staticmethod
    def jigsaw(opts, mesh=None):

        return jigsaw.jigsaw(opts, mesh)

    @staticmethod
    def tetris(opts, nlev, mesh=None):

        return jigsaw.tetris(opts, nlev,
                             mesh)

    @staticmethod
    def icosahedron(opts, nlev, mesh=None):

        return jigsaw.icosahedron(
            opts, nlev, mesh)

    @staticmethod
    def cubedsphere(opts, nlev, mesh=None):

        return jigsaw.cubedsphere(
            opts, nlev, mesh)

    @staticmethod
    def tripod(opts, tria=None):

        return jigsaw.tripod(opts, tria)

    @staticmethod
    def marche(opts, ffun=None):

        return jigsaw.marche(opts, ffun)


class lib:
#--------------------------------- expose api-lib. interface
    @staticmethod
    def jigsaw(opts, geom, mesh, init=None,
               hfun=None):

        return libsaw.jigsaw(opts, geom,
                             mesh,
                             init, hfun)

    @staticmethod
    def tripod(opts, init, tria, geom=None):

        return libsaw.tripod(opts, init,
                             tria, geom)

    @staticmethod
    def marche(opts, ffun):

        return libsaw.marche(opts, ffun)

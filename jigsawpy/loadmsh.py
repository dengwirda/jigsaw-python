
import numpy as np
from pathlib import Path
from jigsawpy.msh_t import jigsaw_msh_t

def loadradii(mesh,fptr,ltag):
    """
    LOADRADII: load the RADII data segment from file.
    
    """
    rtag = ltag[1].split(";")

    mesh.radii = np.empty( \
        +3,dtype=jigsaw_msh_t.REALS_t)

    if   (len(rtag) == +1):    
        mesh.radii[0] = float(rtag[0])
        mesh.radii[1] = float(rtag[0])
        mesh.radii[2] = float(rtag[0])

    elif (len(rtag) == +3):    
        mesh.radii[0] = float(rtag[0])
        mesh.radii[1] = float(rtag[1])
        mesh.radii[2] = float(rtag[2])

    else:
        raise Exception( \
            "Invalid RADII data: "+ ltag)

    return


def loadpoint(mesh,fptr,ltag):
    """
    LOADPOINT: load the POINT data segment from file.
    
    """
    if   (mesh.ndims == +2):
        loadvert2(mesh,fptr,ltag)
    
    elif (mesh.ndims == +3):
        loadvert3(mesh,fptr,ltag)

    else:
        raise Exception( \
            "Invalid NDIMS data: "+ ltag)
    
    return
    
    
def loadvert2(mesh,fptr,ltag):
    """
    LOADVERT2: load the 2-dim. vertex pos. from file.
    
    """
    lnum = int(ltag[1])
    lpos = +0
    
    mesh.vert2 = np.empty( \
        lnum, dtype=jigsaw_msh_t.VERT2_t)

    vpts = mesh.vert2["coord"]
    itag = mesh.vert2["IDtag"]

    while (lnum >= +1):
        data = fptr.readline()
        dtag = data.split(";")
       
        if (len(dtag) == +3):
            vpts[lpos,0] = float(dtag[0])
            vpts[lpos,1] = float(dtag[1])
            
            itag[lpos]   = int  (dtag[2])
        else:
            raise Exception( \
            "Invalid POINT data: "+ data)

        lnum -= +1
        lpos += +1
    
    return
    

def loadvert3(mesh,fptr,ltag):
    """
    LOADVERT3: load the 3-dim. vertex pos. from file.

    """
    lnum = int(ltag[1])
    lpos = +0
    
    mesh.vert3 = np.empty( \
        lnum, dtype=jigsaw_msh_t.VERT3_t)

    vpts = mesh.vert3["coord"]
    itag = mesh.vert3["IDtag"]

    while (lnum >= +1):
        data = fptr.readline()
        dtag = data.split(";")
        
        if (len(dtag) == +4):
            vpts[lpos,0] = float(dtag[0])
            vpts[lpos,1] = float(dtag[1])
            vpts[lpos,2] = float(dtag[2])
            
            itag[lpos]   = int  (dtag[3])
        else:
            raise Exception( \
            "Invalid POINT data: "+ data)

        lnum -= +1
        lpos += +1
        
    return


def loadarray(fptr,ltag):
    """
    LOADARRAY: load the ARRAY data segment from file.
    
    """
    vtag = ltag[ 1].split(";")

    lnum = int(vtag[0])
    vnum = int(vtag[1])
    lpos = +0

    vals = np.empty( \
       [lnum,vnum],dtype=jigsaw_msh_t.REALS_t)

    while (lnum >= +1):
        data = fptr.readline()
        dtag = data.split(";")
        
        for dpos in range(len(dtag)):
            vals[lpos,dpos]= float(dtag[dpos])
        
        lnum -= +1
        lpos += +1

    return vals


def loadpower(mesh,fptr,ltag):
    """
    LOADPOWER: load the POWER data segment from file.
    
    """   
    mesh.power = loadarray(fptr,ltag)

    return


def loadvalue(mesh,fptr,ltag):
    """
    LOADVALUE: load the VALUE data segment from file.
    
    """
    mesh.value = loadarray(fptr,ltag)

    return


def loadslope(mesh,fptr,ltag):
    """
    LOADSLOPE: load the SLOPE data segment from file.
    
    """
    mesh.slope = loadarray(fptr,ltag)
        
    return


def loadedge2(mesh,fptr,ltag):
    """
    LOADEDGE2: load the EDGE2 data segment from file.
    
    """
    lnum = int(ltag[1])
    lpos = +0

    mesh.edge2 = np.empty( \
        lnum, dtype=jigsaw_msh_t.EDGE2_t)

    cell = mesh.edge2["index"]
    itag = mesh.edge2["IDtag"]

    while (lnum >= +1):
        data = fptr.readline()
        dtag = data.split(";")

        if (len(dtag) == +3):        
            cell[lpos,0] = int  (dtag[0])
            cell[lpos,1] = int  (dtag[1])
            
            itag[lpos]   = int  (dtag[2])
        else:
            raise Exception( \
            "Invalid EDGE2 data: "+ data)

        lnum -= +1
        lpos += +1
        
    return
        
        
def loadtria3(mesh,fptr,ltag):
    """
    LOADTRIA3: load the TRIA3 data segment from file.
    
    """
    lnum = int(ltag[1])
    lpos = +0
    
    mesh.tria3 = np.empty( \
        lnum, dtype=jigsaw_msh_t.TRIA3_t)

    cell = mesh.tria3["index"]
    itag = mesh.tria3["IDtag"]

    while (lnum >= +1):
        data = fptr.readline()
        dtag = data.split(";")
        
        if (len(dtag) == +4):
            cell[lpos,0] = int  (dtag[0])
            cell[lpos,1] = int  (dtag[1])
            cell[lpos,2] = int  (dtag[2])
            
            itag[lpos]   = int  (dtag[3])
        else:
            raise Exception( \
            "Invalid TRIA3 data: "+ data)

        lnum -= +1
        lpos += +1
        
    return
        
        
def loadquad4(mesh,fptr,ltag):
    """
    LOADUAD4: load the QUAD4 data segment from file.
    
    """
    lnum = int(ltag[1])
    lpos = +0
    
    mesh.quad4 = np.empty( \
        lnum, dtype=jigsaw_msh_t.QUAD4_t)

    cell = mesh.quad4["index"]
    itag = mesh.quad4["IDtag"]

    while (lnum >= +1):
        data = fptr.readline()
        dtag = data.split(";")
        
        if (len(dtag) == +5):
            cell[lpos,0] = int  (dtag[0])
            cell[lpos,1] = int  (dtag[1])
            cell[lpos,2] = int  (dtag[2])
            cell[lpos,3] = int  (dtag[3])
            
            itag[lpos]   = int  (dtag[4])
        else:
            raise Exception( \
            "Invalid QUAD4 data: "+ data)

        lnum -= +1
        lpos += +1
        
    return
        
        
def loadtria4(mesh,fptr,ltag):
    """
    LOADTRIA4: load the TRIA4 data segment from file.
    
    """
    lnum = int(ltag[1])
    lpos = +0
    
    mesh.tria4 = np.empty( \
        lnum, dtype=jigsaw_msh_t.TRIA4_t)

    cell = mesh.tria4["index"]
    itag = mesh.tria4["IDtag"]

    while (lnum >= +1):
        data = fptr.readline()
        dtag = data.split(";")
    
        if (len(dtag) == +5):     
            cell[lpos,0] = int  (dtag[0])
            cell[lpos,1] = int  (dtag[1])
            cell[lpos,2] = int  (dtag[2])
            cell[lpos,3] = int  (dtag[3])
            
            itag[lpos]   = int  (dtag[4])
        else:
            raise Exception( \
            "Invalid TRIA4 data: "+ data)

        lnum -= +1
        lpos += +1
        
    return
    
    
def loadhexa8(mesh,fptr,ltag):
    """
    LOADHEXA8: load the HEXA8 data segment from file.
    
    """
    lnum = int(ltag[1])
    lpos = +0
    
    mesh.hexa8 = np.empty( \
        lnum, dtype=jigsaw_msh_t.HEXA8_t)

    cell = mesh.hexa8["index"]
    itag = mesh.hexa8["IDtag"]

    while (lnum >= +1):
        data = fptr.readline()
        dtag = data.split(";")
        
        if (len(dtag) == +9):
            cell[lpos,0] = int  (dtag[0])
            cell[lpos,1] = int  (dtag[1])
            cell[lpos,2] = int  (dtag[2])
            cell[lpos,3] = int  (dtag[3])
            cell[lpos,4] = int  (dtag[4])
            cell[lpos,5] = int  (dtag[5])
            cell[lpos,6] = int  (dtag[6])
            cell[lpos,7] = int  (dtag[7])
            
            itag[lpos]   = int  (dtag[8])
        else:
            raise Exception( \
            "Invalid HEXA8 data: "+ data)

        lnum -= +1
        lpos += +1
        
    return


def loadpyra5(mesh,fptr,ltag):
    """
    LOADPYRA5: load the PYRA5 data segment from file.
    
    """
    lnum = int(ltag[1])
    lpos = +0
    
    mesh.pyra5 = np.empty( \
        lnum, dtype=jigsaw_msh_t.PYRA5_t)

    cell = mesh.pyra5["index"]
    itag = mesh.pyra5["IDtag"]

    while (lnum >= +1):
        data = fptr.readline()
        dtag = data.split(";")
        
        if (len(dtag) == +6):
            cell[lpos,0] = int  (dtag[0])
            cell[lpos,1] = int  (dtag[1])
            cell[lpos,2] = int  (dtag[2])
            cell[lpos,3] = int  (dtag[3])
            cell[lpos,4] = int  (dtag[4])
            
            itag[lpos]   = int  (dtag[5])
        else:
            raise Exception( \
            "Invalid PYRA5 data: "+ data)

        lnum -= +1
        lpos += +1
        
    return


def loadwedg6(mesh,fptr,ltag):
    """
    LOADWEDG6: load the WEDG6 data segment from file.
    
    """
    lnum = int(ltag[1])
    lpos = +0
    
    mesh.wedg6 = np.empty( \
        lnum, dtype=jigsaw_msh_t.WEDG6_t)

    cell = mesh.wedg6["index"]
    itag = mesh.wedg6["IDtag"]

    while (lnum >= +1):
        data = fptr.readline()
        dtag = data.split(";")
        
        if (len(dtag) == +7):
            cell[lpos,0] = int  (dtag[0])
            cell[lpos,1] = int  (dtag[1])
            cell[lpos,2] = int  (dtag[2])
            cell[lpos,3] = int  (dtag[3])
            cell[lpos,4] = int  (dtag[4])
            cell[lpos,5] = int  (dtag[5])
            
            itag[lpos]   = int  (dtag[6])
        else:
            raise Exception( \
            "Invalid WEDG6 data: "+ data)

        lnum -= +1
        lpos += +1
        
    return


def loadbound(mesh,fptr,ltag):
    """
    LOADBOUND: load the BOUND data segment from file.
    
    """
    lnum = int(ltag[1])
    lpos = +0
    
    mesh.bound = np.empty( \
        lnum, dtype=jigsaw_msh_t.BOUND_t)

    itag = mesh.bound["IDtag"]
    indx = mesh.bound["index"]
    kind = mesh.bound["cells"]

    while (lnum >= +1):
        data = fptr.readline()
        dtag = data.split(";")
    
        if (len(dtag) == +3):
            itag[lpos]   = int  (dtag[0])
            indx[lpos]   = int  (dtag[1])
            kind[lpos]   = int  (dtag[2])
        else:
            raise Exception( \
            "Invalid BOUND data: "+ data)

        lnum -= +1
        lpos += +1
        
    return


def loadcoord(mesh,fptr,ltag):
    """
    LOADCOORD: load the COORD data segment from file.
    
    """
    ctag = ltag[1].split(";")

    idim = int(ctag[0])
    lnum = int(ctag[1])
    lpos = +0
    
    mesh.ndims = max(mesh.ndims,idim)

    if   (idim == +1):
        mesh.xgrid = np.empty( \
            lnum,dtype=jigsaw_msh_t.REALS_t)

        data = mesh.xgrid[:]

    elif (idim == +2):
        mesh.ygrid = np.empty( \
            lnum,dtype=jigsaw_msh_t.REALS_t)

        data = mesh.ygrid[:]

    elif (idim == +3):
        mesh.zgrid = np.empty( \
            lnum,dtype=jigsaw_msh_t.REALS_t)

        data = mesh.zgrid[:]

    while (lnum >= +1):
        data[lpos] = float(fptr.readline ())
    
        lnum -= +1
        lpos += +1

    return
      
        
def loadlines(mesh,fptr,line):
    """
    LOADLINES: load the next non-null line from file.
    
    """
    
    #------------------------------ skip any 'comment' lines
   
    if (line[0] != '#'):
    
    #------------------------------ split about '=' charact.
        ltag = line.split("=")
        kind = ltag[0].upper()
        
        if   (kind == "MSHID"):
        
    #----------------------------------- parse MSHID struct.
            data = ltag[1].split(";")

            if (len(data) > 1):
                mesh.mshID = \
            data[1].strip().lower()
            
        elif (kind == "NDIMS"):
        
    #----------------------------------- parse NDIMS struct.
            mesh.ndims = int(ltag[1])
        
        elif (kind == "RADII"):
    
    #----------------------------------- parse RADII struct.
            loadradii(mesh,fptr,ltag)
    
        elif (kind == "POINT"):
    
    #----------------------------------- parse POINT struct.
            loadpoint(mesh,fptr,ltag)

        elif (kind == "POWER"):
    
    #----------------------------------- parse POWER struct.
            loadpower(mesh,fptr,ltag)

        elif (kind == "VALUE"):
   
    #----------------------------------- parse VALUE struct.
            loadvalue(mesh,fptr,ltag)

        elif (kind == "SLOPE"):
   
    #----------------------------------- parse SLOPE struct.
            loadslope(mesh,fptr,ltag)
                
        elif (kind == "EDGE2"):
        
    #----------------------------------- parse EDGE2 struct.
            loadedge2(mesh,fptr,ltag)
                
        elif (kind == "TRIA3"):
   
    #----------------------------------- parse TRIA3 struct.
            loadtria3(mesh,fptr,ltag)
                
        elif (kind == "QUAD4"):
   
    #----------------------------------- parse QUAD4 struct.
            loadquad4(mesh,fptr,ltag)
                
        elif (kind == "TRIA4"):
   
    #----------------------------------- parse TRIA4 struct.
            loadtria4(mesh,fptr,ltag)
                
        elif (kind == "HEXA8"):
   
    #----------------------------------- parse HEXA8 struct.
            loadhexa8(mesh,fptr,ltag)

        elif (kind == "PYRA5"):
   
    #----------------------------------- parse PYRA5 struct.
            loadpyra5(mesh,fptr,ltag)

        elif (kind == "WEDG6"):
   
    #----------------------------------- parse WEDG6 struct.
            loadwedg6(mesh,fptr,ltag)

        elif (kind == "BOUND"):
   
    #----------------------------------- parse BOUND struct.
            loadbound(mesh,fptr,ltag)

        elif (kind == "COORD"):
   
    #----------------------------------- parse COORD struct.
            loadcoord(mesh,fptr,ltag)
        
    return


def loadmsh(name,mesh):
    """
    LOADMSH: load a JIGSAW MSH obj. from file.

    LOADMSH(NAME,MESH)

    MESH is JIGSAW's primary mesh/grid/geom class. See MSH_t
    for details.

    Data in MESH is loaded on-demand -- any objects included
    in the file will be read.
    
    """

    if (not isinstance(name,str)):
        raise Exception("Incorrect type: NAME.")
        
    if (not isinstance(mesh,jigsaw_msh_t)):
        raise Exception("Incorrect type: MESH.")

    with Path(name).open("r") as fptr:
        while (True):
        
    #--------------------------- get the next line from file    
            line = fptr.readline ()
            
            if (len(line) != +0):

    #--------------------------- parse next non-null section
                loadlines(
                    mesh,fptr,line)                    
            
            else:
    #--------------------------- reached end-of-file: done!!
                break

    if (mesh.value is not None and \
            mesh.value.size != +0):
    #--------------------------- finalise VALUE.shape layout
        if (mesh.ndims == +2 and \
            mesh.xgrid is not None and \
            mesh.xgrid.size != +0  and \
            mesh.ygrid is not None and \
            mesh.ygrid.size != +0):
    #--------------------------- reshape data to 2-dim array
            nnum = mesh.xgrid.size \
                 * mesh.ygrid.size

            nval = mesh.value.size \
                // nnum

            mesh.value = \
                 np.squeeze(np.reshape(mesh.value, 
                (mesh.ygrid.size, 
                 mesh.xgrid.size,
                 nval), order="F") )

        if (mesh.ndims == +3 and \
            mesh.xgrid is not None and \
            mesh.xgrid.size != +0  and \
            mesh.ygrid is not None and \
            mesh.ygrid.size != +0  and \
            mesh.zgrid is not None and \
            mesh.zgrid.size != +0):
    #--------------------------- reshape data to 3-dim array
            nnum = mesh.xgrid.size \
                 * mesh.ygrid.size \
                 * mesh.zgrid.size

            nval = mesh.value.size \
                // nnum

            mesh.value = \
                 np.squeeze(np.reshape(mesh.value, 
                (mesh.ygrid.size, 
                 mesh.xgrid.size,
                 mesh.zgrid.size,
                 nval), order="F") )

    if (mesh.slope is not None and \
            mesh.slope.size != +0):
    #--------------------------- finalise SLOPE.shape layout
        if (mesh.ndims == +2 and \
            mesh.xgrid is not None and \
            mesh.xgrid.size != +0  and \
            mesh.ygrid is not None and \
            mesh.ygrid.size != +0):
    #--------------------------- reshape data to 2-dim array
            nnum = mesh.xgrid.size \
                 * mesh.ygrid.size

            nval = mesh.slope.size \
                // nnum

            mesh.slope = \
                 np.squeeze(np.reshape(mesh.slope, 
                (mesh.ygrid.size, 
                 mesh.xgrid.size,
                 nval), order="F") )

        if (mesh.ndims == +3 and \
            mesh.xgrid is not None and \
            mesh.xgrid.size != +0  and \
            mesh.ygrid is not None and \
            mesh.ygrid.size != +0  and \
            mesh.zgrid is not None and \
            mesh.zgrid.size != +0):
    #--------------------------- reshape data to 3-dim array
            nnum = mesh.xgrid.size \
                 * mesh.ygrid.size \
                 * mesh.zgrid.size

            nval = mesh.slope.size \
                // nnum

            mesh.slope = \
                 np.squeeze(np.reshape(mesh.slope, 
                (mesh.ygrid.size, 
                 mesh.xgrid.size,
                 mesh.zgrid.size,
                 nval), order="F") )

    return




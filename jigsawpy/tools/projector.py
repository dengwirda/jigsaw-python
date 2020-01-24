
import numpy as np

def stereo3_f(rrad,xpos,ypos,xmid,ymid):
    """
    STEREO3_f: compute the forward stereographic projection.
    
    """

    #------------------------------------ do forward mapping
    
    kden = +1. + np.sin(ymid)*np.sin(ypos) + \
      np.cos(ymid)*np.cos(ypos)*np.cos(xpos-xmid)
    
    kval = +2. * rrad / kden ** 1

    dval = -2. * rrad / kden ** 2
    
    xnew = kval* np.cos(ypos)*np.sin(xpos-xmid)
    ynew = kval*(np.cos(ymid)*np.sin(ypos) - \
      np.sin(ymid)*np.cos(ypos)*np.cos(xpos-xmid))

    #------------------------------------ compute indicatrix

    dkdy = dval*(np.sin(ymid)*np.cos(ypos) - \
      np.cos(ymid)*np.sin(ypos)*np.cos(xpos-xmid))
    
    dXdy = dkdy*np.cos(ypos)*np.sin(xpos-xmid) \
         - kval*np.sin(ypos)*np.sin(xpos-xmid)
  
    dYdy = dkdy*(np.cos(ymid)*np.sin(ypos) - \
      np.sin(ymid)*np.cos(ypos)*np.cos(xpos-xmid)) \
         + kval*(np.cos(ymid)*np.cos(ypos) + \
      np.sin(ymid)*np.sin(ypos)*np.cos(xpos-xmid))
    
    scal = +1./rrad * np.sqrt(dXdy**2+dYdy**2)

    return xnew, ynew, scal


def stereo3_i(rrad,xpos,ypos,xmid,ymid):
    """
    STEREO3_i: compute the inverse stereographic projection.
    
    """

    #------------------------------------ do inverse mapping

    rval = np.sqrt(xpos**2 + ypos**2)
    rval = np.maximum(1.E-16*np.max(rval), rval)
      
    cval = +2. * np.arctan2(rval, +2. * rrad)
        
    xnew = xmid + np.arctan2(xpos*np.sin(cval) , \
        rval * np.cos(ymid) * np.cos(cval) \
      - ypos * np.sin(ymid) * np.sin(cval) )
      
    ynew = np.arcsin(np.cos(cval)*np.sin(ymid) + \
       (ypos*np.sin(cval)*np.cos(ymid)) / rval)

    #------------------------------------ compute indicatrix

    kden = +1. + np.sin(ymid)*np.sin(ynew) + \
      np.cos(ymid)*np.cos(ynew)*np.cos(xnew-xmid)
    
    dval = -2. * rrad / kden ** 2
 
    kval = +2. * rrad / kden ** 1
    
    dkdy = dval*(np.sin(ymid)*np.cos(ynew) - \
      np.cos(ymid)*np.sin(ynew)*np.cos(xnew-xmid))
    
    dXdy = dkdy*np.cos(ynew)*np.sin(xnew-xmid) \
         - kval*np.sin(ynew)*np.sin(xnew-xmid)
  
    dYdy = dkdy*(np.cos(ymid)*np.sin(ynew) - \
      np.sin(ymid)*np.cos(ynew)*np.cos(xnew-xmid)) \
         + kval*(np.cos(ymid)*np.cos(ynew) + \
      np.sin(ymid)*np.sin(ynew)*np.cos(xnew-xmid))
    
    scal = rrad * +1./np.sqrt(dXdy**2+dYdy**2)

    return xnew, ynew, scal


def stereo3(rrad,xpos,ypos,xmid,ymid,kind):
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
 
    SCAL is the scale-factor associated with the forward ma-
    pping. This array stores the relative length distortion 
    induced by the projection for all points in [XNEW,YNEW].

    """

    if   (kind.lower() == "fwd"):

        xnew, ynew, scal = \
            stereo3_f(rrad,xpos,ypos,xmid,ymid)

    elif (kind.lower() == "inv"):
    
        xnew, ynew, scal = \
            stereo3_i(rrad,xpos,ypos,xmid,ymid)


    return xnew, ynew, scal




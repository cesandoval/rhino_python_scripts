import os
import Rhino
import cPickle as pickle
import rhinoscriptsyntax as rs
from scriptcontext import doc

sid= 302
path = 'E:/db/'
pickle_list = [
        #'benchmeshes',
        'billboards',
        'canopybreps',
        'canopymeshes',
        #'benchsolids',
        #'groundsurface',
        #'groundchunk',
        'drainareamesh',
        #'fullterrainmesh',
        #'activebusstops',
        'siteoutline',
        #'drainarrows',
        #'billboards',
        'drainareaoutlines',
        #'hardscapeputlines',
        #'parcels',
        #'hardscapemesh'
        #'accessedges',
        #'pathsourcepins',
        #'pathdestpin',
        'pathways',
        #'weightedhardscapecircles',
        #'hardgriddots',
        #'benchlines',
        #'benchradii',
        #'bigcontours',
        #'smallcontours',
        #'draincurves',
        #'plantgriddots',
        #'weightedplantingcircles',
        #'plantwindow1point5',
        #'plantwindow3point0',
        #'plantwindow4point5',
        #'plantwindow6point0',
        #'plantwindow7point5',
        #'plantwindow8point0',
        #'plantwindow9point5',
        #'plantwindow12point0',
        #'plantwindow15point0',
        #'plantwindow18point0',
        'view',
        ]

def setView( sid ):
    # still don't know how to set up the size of the viewport.
    # this needs to be done manually
    f = open(path + '%sview' % sid, 'rb')
    view = pickle.load(f)
    f.close()
    if len(view) == 3:
        geom = view[0]
        vect = Rhino.Geometry.Vector3d(view[1])
        targ = view[2]
    else:
        return 'bad view data'

    vp = doc.Views.ActiveView.ActiveViewport
    vp.SetCameraDirection( vect, True)
    vp.SetCameraTarget(targ, True)
    bb = geom.GetBoundingBox(True)
    vp.ZoomBoundingBox( bb)
    doc.Views.ActiveView.Redraw()
    return view

def read_pickles(path, pickle_list, sid):
    for layer in pickle_list:
        try:
            f = open(path + '%s%s' %(sid, layer), 'rb')
            a = pickle.load(f)
            f.close()
            print a
        except:
            print 'problem loading %s: file may not exist' % path
    
# SID can be a range of numbers to loop through all views
setView(sid)
z_distance = setView(sid)[2].Z
print z_distance
read_pickles(path, pickle_list, sid) 
print read_pickles
import os
import time

import Rhino
import cPickle as pickle
import rhinoscriptsyntax as rs
from scriptcontext import doc

#sid= 766 # I need to remove this... just testing 
pathy = 'E:/db/'
rhino_folder = 'C:/LocalCode_LA/rhino'
outpath = "C:\\LocalCode_LA\\renders\\"
#outpath = "C:\\LocalCode_LA\\renders\\somewhere.png"

def setView( sid, path ):
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

def batch_render(rhino_folder, outpath):
    #rhino_files = os.listdir(rhino_folder)
    rhino_l = []
    directory = os.listdir(rhino_folder)
    for f in directory:
        if f.endswith(".3dm"):
            rhino_l.append(f)
    rhino_list = sorted([int(i[:-4]) for i in rhino_l])
    rhino_files = [str(i) + '.3dm' for i in rhino_list]
    
    i = 0
    for file in rhino_files:
        if file.endswith(".3dm"):
            i += 1
            path = os.path.join(rhino_folder,file)
            #print path
            rs.Command("_-Open " + path)
            
            # Set view
            setView(i,pathy)
            if setView:
                print 1
            filename = outpath + str(i) + '.png'
            print filename
            # then render view...
            
            # Steve's way
            #rs.Command("_Render")
            #time.sleep(10)
            #rs.Command("_SaveRenderWindowAs " + str(filename))
            #rs.Command("_CloseRenderWindow")
            
            # Ben's
            Rhino.RhinoApp.RunScript("_-Render", False)
            time.sleep(10)# number of seconds to wait
            Rhino.RhinoApp.RunScript("_-SaveRenderWindowAs \n\"" + filename + "\"\n", False)
            Rhino.RhinoApp.RunScript("_-CloseRenderWindow", False)


#Rhino.RhinoApp.RunScript("_-Render", False)
#time.sleep(10) # number of seconds to wait

#Rhino.RhinoApp.RunScript("_-CloseRenderWindow", False)

# SID can be a range of numbers to loop through all views
if __name__=="__main__":
    #BatchMaterialTexture(image_folder, rhino_folder)
    batch_render(rhino_folder, outpath)

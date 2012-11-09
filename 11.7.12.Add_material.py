import Rhino
import scriptcontext
from rhinoscript import utility as rhutil
import rhinoscriptsyntax as rs
import os

image_folder = 'C:/LocalCode_LA/images'
rhino_folder = 'C:/LocalCode_LA/rhino'

def AddMaterial(image_path):
    # materials are stored in the document's material table
    index = scriptcontext.doc.Materials.Add()
    mat = scriptcontext.doc.Materials[index]
    mat.SetBitmapTexture(image_path)
    mat.CommitChanges()
    
    # Set Material Attributes to Geometry
    attr = Rhino.DocObjects.ObjectAttributes()
    attr.MaterialIndex = index
    attr.MaterialSource = Rhino.DocObjects.ObjectMaterialSource.MaterialFromObject
    return attr

def AddMaterialToObject(object_id, attr):
    # Assigns Texture to geometry
    object_id = rhutil.coerceguid(object_id)
    if( object_id==None ): return scriptcontext.errorhandler()
    
    objref = Rhino.DocObjects.ObjRef(object_id)
    rhino_object = objref.Object()
    objref.Dispose()
    if( rhino_object==None ): return scriptcontext.errorhandler()

    scriptcontext.doc.Objects.ModifyAttributes(rhino_object, attr, True)
    scriptcontext.doc.Views.Redraw();

def BatchMaterialTexture(image_folder, rhino_folder):
    #images_list = os.listdir(image_folder)
    #rhino_files = os.listdir(rhino_folder)
    images_l = sorted([int(i[:-4]) for i in os.listdir(image_folder)])
    images_list = [str(i) + '.jpg' for i in images_l]
    
    rhino_list = sorted([int(i[:-4]) for i in os.listdir(rhino_folder)])
    rhino_files = [str(i) + '.3dm' for i in rhino_list]
    i = -1
    for file in rhino_files:
        if file.endswith(".3dm"):
            i += 1
            path = os.path.join(rhino_folder,file)
            rs.Command("_-Open " + path)
            
            site = rs.AllObjects()
            AddMaterialToObject(site, AddMaterial(image_folder + "/" + images_list[i]))
            
            rs.DocumentModified(False)
            rs.Command("_Save")
            
            rs.DocumentModified(False)
            rs.Command("_-New _None")

if __name__=="__main__":
    BatchMaterialTexture(image_folder, rhino_folder)

    


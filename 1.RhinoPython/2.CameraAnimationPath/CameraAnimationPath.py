#coding=utf-8
import System.Drawing as sd
import string as s
import Rhino.Geometry as rg
from Rhino.RhinoMath import UnsetIntIndex
import BubalusLib  as bu
import Rhino.RhinoDoc as rr
import Rhino.DocObjects as rd
from System.Collections.Generic import IEnumerable
import System.Windows.Forms as form

doc = rr.ActiveDoc

#Create a layer,Return the index of the layer.
def MyAddLayer(layerName = "CameraPath",cameraLocation = "Location",cameraTarget = "Target"):
    result = []
    layers = doc.Layers
    layersNames = [layer.FullPath for layer in layers if not layer.IsDeleted]
    
    lists = [layerName,layerName+"::"+cameraLocation,layerName+"::"+cameraTarget]
    colors = [sd.Color.Black,sd.Color.Red,sd.Color.Blue]
    for i in xrange(3):
        if(lists[i] in layersNames):
            layer_index = layers.FindByFullPath(lists[i], UnsetIntIndex)
            result.append(layer_index)
            continue
        else:
            if(i):
                child_name = s.split(lists[i],"::")[-1]
                childlayer = rd.Layer()
                childlayer.ParentLayerId = layers.FindIndex(result[0]).Id
                childlayer.Name = child_name
                childlayer.Color = colors[i]
                layer_index = layers.Add(childlayer);
                result.append(layer_index)
            else:
                layer_index = layers.Add(lists[i],colors[i])
                result.append(layer_index)
    return result


def AddCameraCurve(layers):
    """
    Create camera paths based on named views.
    """
    
    #get named views
    named_views = doc.NamedViews
    view_names = []
    if(named_views.Count):
        items = [[named_view.Name,False] for named_view in named_views]
        results = (bu.MyCheckBoxList(items, "Please select the views for generating the camera animation paths.","Named views")).ShowMyCheckBoxList()
        if(results):view_names = [item[0] for item in results if(item[1]==True)]
    
    
    if(not view_names or None):return None
    
    #Retrieve camera location points of named viewports.
    named_views = [named_view for named_view in named_views if(named_view.Name in view_names)]
    Location_Points = []
    Target_Points = []
    for named_view in named_views:
        camera_location = named_view.Viewport.CameraLocation
        camera_target = named_view.Viewport.TargetPoint
        if(camera_location not in Location_Points):
            Location_Points.append(camera_location )
        if(camera_target not in Target_Points):
            Target_Points.append(camera_target)
    
    if(len(Location_Points)<2 or len(Target_Points )<2):
        for layer in layers:doc.Layers.Delete(layer,False)
        form.MessageBox.Show("You must select two or more views.")
        return None
    #Create a curve ,bake
    location_attr = rd.ObjectAttributes()
    location_attr.LayerIndex = layers[1]
    
    target_attr = rd.ObjectAttributes()
    target_attr.LayerIndex = layers[2]
    
    doc.Objects.AddPoints.Overloads[IEnumerable[rg.Point3d],rd.ObjectAttributes ](Location_Points,location_attr)
    doc.Objects.AddPoints.Overloads[IEnumerable[rg.Point3d],rd.ObjectAttributes ](Target_Points,target_attr)
    
    location_curve = rg.NurbsCurve.CreateInterpolatedCurve(Location_Points,5,rg.CurveKnotStyle.UniformPeriodic)
    doc.Objects.AddCurve(location_curve,location_attr)
    
    target_curve = rg.NurbsCurve.CreateInterpolatedCurve(Target_Points,5,rg.CurveKnotStyle.UniformPeriodic)
    doc.Objects.AddCurve(target_curve,target_attr)
    



def main():
    doc.Views.EnableRedraw(False,False,False)
    layers = MyAddLayer()
    AddCameraCurve(layers)
    doc.Views.EnableRedraw(True,True,True)

if __name__ == "__main__":
    main()
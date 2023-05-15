from ghpythonlib.componentbase import executingcomponent as component
import System.Drawing as sd
import Rhino.Geometry as rg

class MyComponent(component):
    lines = []
    colors = []
    
    def RunScript(self, pt, vec, color):
        if not pt :return 
        if not vec :return
        self.lines.append(rg.Line(pt,pt+vec))
        if not color:
            self.colors.append(sd.Color.Red)
        else:
            self.colors.append(color)
    def DrawViewportWires(self,args):
        count = len(self.lines)
        for i in xrange(count):
            args.Display.DrawArrow(self.lines[i],self.colors[i])
    
    
    def GetBoundingBox(self):
        if len(self.lines) == None:
            return rg.BoundingBox.Empty
        else:
            self.box = rg.BoundingBox.Unset
            for line in self.lines:
                self.box.Union(line.BoundingBox)
            return self.box
    
    def get_ClippingBox(self):
        return self.GetBoundingBox()
    
    def BeforeSolveInstance(self):
        self.lines = []
        self.colors = []
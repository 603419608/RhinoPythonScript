#coding=utf-8
import rhinoscriptsyntax as rs
import string as s


def select_Text(rhino_objects, geometry, geometry_index):
    return rs.IsTextDot(geometry) or rs.IsText(geometry)

def ReplaceText(text,oldText,newText):
    if (s.find(text,oldText)!=-1):
        return text.replace(oldText,newText)

def ChangeText(oldText,newText):
    geometrys = rs.GetObjects("Select the text and dot to be replaced.",0,True,True,custom_filter = select_Text)
    rs.EnableRedraw(False)
    if(geometrys):
        for i in geometrys:
            if(rs.IsTextDot(i)):
                string1 = rs.TextDotText(i)
                string2 = ReplaceText(string1,oldText,newText)
                rs.TextDotText(i,string2)
            else:
                string1 = rs.TextObjectText(i)
                string2 = ReplaceText(string1,oldText,newText)
                rs.TextObjectText(i,string2)
    else:
        print("No text and dot selected.")
    rs.EnableRedraw(True)

        

if __name__=="__main__":
    ChangeText("XXM","VM")
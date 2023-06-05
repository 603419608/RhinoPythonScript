#coding=utf-8
import Eto.Forms as forms
import Rhino.UI
import Eto.Drawing as drawing

"""
The purpose of the MyCheckBoxList class is similar to the rs.CheckListBox() method in RhinoPython.
The only difference is that it includes an added sorting functionality.
input:
    items : ([[str, bool], ...]):  a list of tuples containing a string and a boolean check state
    message : (str, optional):   a prompt or message
    title : str, optional):   a dialog box title
    
outPut:
    list((str, bool), ...)of tuples containing the input string in items along with their new boolean check value
    None: on error
 
"""

class MyCheckBoxList(forms.Dialog[bool]):
    
    def __init__(self,items,message=None,title=None):
        self.Padding = drawing.Padding(5)
        self.Resizable = False
        self.Title = title
        self.selectcheckbox = items
        self.order_selectcheckbox = []
        
        #return
        self.output = False
        
        
        #Set form prompt
        self.Label1 = forms.Label(Text = message)
        
        #Create check boxes
        self.checkboxes = [forms.CheckBox(Text=item[0], Checked=item[1]) for item in items if item]
        
        #checkbox.CheckedChanged  event
        for checkbox in self.checkboxes:
            checkbox.CheckedChanged += self.OrderSelectCheckBox
        
        self.selectall= forms.Button(Text = 'Select All')
        self.selectall.Click += self.OnSelectAllButtonClick
        
        
        self.DefaultButton = forms.Button(Text = 'OK')
        self.DefaultButton.Click += self.OnOKButtonClick
        self.AbortButton = forms.Button(Text = 'Cancel')
        self.AbortButton.Click += self.OnCloseButtonClick
        
        
        #Layout
        layout = forms.DynamicLayout()
        layout.Spacing = drawing.Size(5,5)
        layout.AddRow(self.Label1)
        layout.AddRow(None)
        
        for checkbox  in self.checkboxes:
            layout.AddRow(checkbox)
        
        layout.AddRow(None)
        layout.AddRow(None,self.selectall)
        layout.AddRow(None)
        layout.AddRow(self.DefaultButton, self.AbortButton)
        layout.AddRow(None)
        
        self.Content = layout
        
    def ShowMyCheckBoxList(self):
        self.ShowModal(Rhino.UI.RhinoEtoApp.MainWindow)
        
        list = []
        #Output return value based on conditions
        if(self.output):
            self.order_selectcheckbox.reverse()
            result = [[check.Text,check.Checked] for check in self.order_selectcheckbox if check]
            list = [check for check in self.selectcheckbox if(check not in result)]
            list.extend(result)
        return list
    
    
    #event func 
    def OnOKButtonClick(self, sender, e):
        self.Close(True)
        self.output = True
    
    def OnCloseButtonClick(self, sender, e):
        self.Close(False)
    
    
    def OnSelectAllButtonClick(self, sender, e):
        for checkbox  in self.checkboxes:
            checkbox.Checked = True
    
    
    def OrderSelectCheckBox(self, sender, e):
        """
        Sort based on the state of checkboxes
        """
        for i,checkbox in enumerate(self.checkboxes):
            if(self.selectcheckbox[i][1] == self.checkboxes[i].Checked):continue
            
            if(checkbox.Checked):
                self.order_selectcheckbox.insert(0,checkbox)
            elif(checkbox in self.order_selectcheckbox):
                self.order_selectcheckbox.remove(checkbox)
            break
        
        self.selectcheckbox = [[check.Text,check.Checked] for check in self.checkboxes]


if __name__ == "__main__":
    items = [["box1",False],["box2",True],["box3",False],["box4",False],["box5",True],["box6",False],["box7",False]]
    checklistboxs = MyCheckBoxList(items,"Test","Testing the MyCheckBoxList class")
    result =  checklistboxs.ShowMyCheckBoxList()
    if result:
        for item in result:
            if(item[1] ):print item[0]
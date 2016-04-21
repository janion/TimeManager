'''
Created on 21 Apr 2016

@author: Janion
'''

import wx

class ClaimedHoursDlg(wx.Dialog):
    
    def __init__(self, parent, idd, logic, index=-1):        
        wx.Dialog.__init__(self, parent, idd, "Claim hours", size=(300, 300),
                           style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
                           )
        self.panel = wx.Panel(self, -1)
        self.SetMinSize(self.GetSize())
        
        self.logic = logic
        
        #Create text and choice box for the project to work on
        wx.StaticText(self.panel, -1, "Please select the project to view:",
                      (10, 10)
                      )
        self.proj_choice = wx.Choice(self.panel, pos=(10, 30), size=(230, -1),
                                     choices=self.logic.getProjectNames()
                                     )
        
        
        self.checkList = wx.CheckListBox(self.panel, -1, choices=[], pos=(10, 60))
        
        self.saveBtn = wx.Button(self.panel, -1, 'Save')
        self.cancelBtn = wx.Button(self.panel, -1, 'Cancel')
        
        #Bind events
        self.Bind(wx.EVT_CHOICE, self.populateList, self.proj_choice)
        self.Bind(wx.EVT_SIZE, self.resize)
        self.Bind(wx.EVT_BUTTON, self.save, self.saveBtn)
        self.Bind(wx.EVT_BUTTON, self.close, self.cancelBtn)
        
        if index != -1:
            self.proj_choice.SetSelection(index)
            self.populateList(None)

################################################################################
    
    def resize(self, event):
        event.Skip()
        size = self.GetSize()
        
        self.proj_choice.SetSize((size[0] - 40, -1))
        self.checkList.SetSize((size[0] - 40, size[1] - 140))
        self.saveBtn.SetPosition((10, self.checkList.GetSize()[1] + self.checkList.GetPosition()[1] + 10))
        self.cancelBtn.SetPosition((size[0] - self.cancelBtn.GetSize()[0] - 30,
                                    self.checkList.GetSize()[1] + self.checkList.GetPosition()[1] + 10
                                    ))
        
################################################################################
        
    def populateList(self, event):
        (items, states) = self.logic.getFormattedData(self.proj_choice.GetStringSelection())
        
        self.checkList.SetItems(items)
        for x in xrange(len(states)):
            self.checkList.Check(x, bool(states[x]))
        
################################################################################
        
    def close(self, event):
        self.Destroy()
        
################################################################################
        
    def save(self, event):
        checked = self.checkList.GetChecked()
        self.logic.setClaimedHours(self.proj_choice.GetStringSelection(), checked)
        self.Destroy()
        
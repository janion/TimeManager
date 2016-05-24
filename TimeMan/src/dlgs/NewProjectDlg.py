# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 15:02:44 2015

@author: erik_
"""

import wx

class NewProjectDlg(wx.Dialog):
    
    def __init__(self, parent, idd, logic):
        wx.Dialog.__init__(self, parent, idd, 'New Project', size=(250, 170))
        self.panel = wx.Panel(self, -1)
        
        self.logic = logic
        
        #Create instructional text and a text box to enter the project name
        wx.StaticText(self.panel, -1, "Please enter the name of the project:",
                      (10, 10)
                      )
        self.proj_name = wx.TextCtrl(self.panel, -1, '', pos=(10, 30),
                                     size=(225, -1)
                                     )
        #Create text and a date picker
        wx.StaticText(self.panel, -1, "Select start date:", (10, 60))
        
        self.datePicker = wx.DatePickerCtrl(self.panel, size=(100, -1), pos=(10, 80),
                                      style = wx.DP_DROPDOWN | wx.DP_SHOWCENTURY
                                      )
        #Create text and hour entry box
        wx.StaticText(self.panel, -1, "Hours:", (120, 60))
        self.hours = wx.SpinCtrl(self.panel, -1, "", pos=(120, 80),
                                 size=(40, -1)
                                 )
        self.hours.SetRange(0, 23)
        self.hours.SetValue(0)
        
        #Create text and hour entry box
        wx.StaticText(self.panel, -1, "Minutes:", (170, 60))
        self.mins = wx.SpinCtrl(self.panel, -1, "", pos=(170, 80), size=(40, -1)
                                )
        self.mins.SetRange(0, 59)
        self.mins.SetValue(0)
        
        #Create buttons to save new project and to cancel the action
        self.save_btn = wx.Button(self.panel, -1, 'Save', pos=(10, 110))
        self.save_btn.Enable(False)
        self.cancel_btn = wx.Button(self.panel, -1, 'Cancel', pos=(150, 110))
        
        #Bind events
        self.Bind(wx.EVT_TEXT, self.validateSelections, self.proj_name)
        self.Bind(wx.EVT_DATE_CHANGED, self.validateSelections, self.datePicker)
        self.Bind(wx.EVT_BUTTON, self.saveProject, self.save_btn)
        self.Bind(wx.EVT_BUTTON, self.close, self.cancel_btn)
        
################################################################################

    def close(self, event):
        self.Destroy()
        
################################################################################

    def validateSelections(self, event):
        validDate = self.validateDatePicker()
        validName = self.validateNameBox()
        
        self.save_btn.Enable(validDate and validName)
        
################################################################################

    def validateDatePicker(self):
        date = self.datePicker.GetValue()
        dateArray = [date.GetDay(), date.GetMonth() + 1, date.GetYear()]

        if self.logic.isDateValid(dateArray):
            self.datePicker.SetForegroundColour((0, 0, 0))
            self.datePicker.Refresh()
            return True
        else:
            self.datePicker.SetForegroundColour((255, 0, 0))
            self.datePicker.Refresh()
            return False
            
        
################################################################################

    def validateNameBox(self): #Enable/disable save button as appropriate
        typedName = self.proj_name.GetValue().strip(" ")
        if self.proj_name.GetValue() != typedName:
            self.proj_name.SetValue(typedName)
            self.proj_name.SetInsertionPointEnd()
        
        nameLimit = self.logic.getProjectNameLimit()
        if len(typedName) > nameLimit:
            self.proj_name.SetValue(typedName[0:nameLimit])
            self.proj_name.SetInsertionPointEnd()
            
        if typedName != '':
            isValid = self.logic.isValidProjectName(typedName)
            
            if isValid:
                self.proj_name.SetForegroundColour((0, 0, 0))
            else:
                self.proj_name.SetForegroundColour((255, 0, 0))
            self.proj_name.Refresh()
            return isValid
                    
        else:
            return False
        
################################################################################

    def saveProject(self, event): #Create project file if name is unique
        name = self.proj_name.GetValue()
        if self.logic.isUniqueProjectName(name):
            #If project name is unique
        
            #Get project number of hours entered and start date
            work_time = round(self.hours.GetValue() +
                              float(self.mins.GetValue()) / 60, 2
                              )

            date = self.datePicker.GetValue()
            dateArray = [date.GetDay(), date.GetMonth() + 1, date.GetYear()]
            
            self.logic.createNewProjectFile(name, dateArray, work_time)
            self.Destroy()
        else:
            #Tell user to enter another name
            dlg2 = wx.MessageDialog(
                self, 'That project name is already in use',
                'Invalid project name', wx.OK | wx.ICON_INFORMATION
                )
            dlg2.ShowModal()
            dlg2.Destroy()
        
        
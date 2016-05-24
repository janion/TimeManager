# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 14:59:28 2015

@author: erik_
"""

import wx

class BackdateDlg(wx.Dialog):
    def __init__(self, parent, idd, logic, projectName):
        wx.Dialog.__init__(self, parent, idd, 'Back date project', size=(250, 170))
        self.parent = parent
        self.panel = wx.Panel(self, -1)
        
        self.logic = logic
        
        #Create text and project choice box
        wx.StaticText(self.panel, -1,
                      "Please select the project to back date:", (10, 10)
                      )
        projectList = self.logic.getProjectNames()
        self.proj_choice = wx.Choice(self.panel, pos=(10, 30), size=(225, -1),
                                     choices=projectList
                                     )
        #Create text and date picker
        wx.StaticText(self.panel, -1, "Select date:", (10, 60))
        self.datePicker = wx.DatePickerCtrl(self.panel, size=(100, -1), pos=(10, 80),
                                      style = wx.DP_DROPDOWN | wx.DP_SHOWCENTURY
                                      )
        #Create text and time input boxes
        wx.StaticText(self.panel, -1, "Hours:", (120, 60))
        self.hours = wx.SpinCtrl(self.panel, -1, "", pos=(120, 80),
                                 size=(40, -1)
                                 )
        self.hours.SetRange(0, 23)
        self.hours.SetValue(0)
        
        wx.StaticText(self.panel, -1, "Minutes:", (170, 60))
        self.mins = wx.SpinCtrl(self.panel, -1, "", pos=(170, 80), size=(40, -1)
                                )
        self.mins.SetRange(0, 59)
        self.mins.SetValue(0)
        
        #Create buttons
        self.log_btn = wx.Button(self.panel, -1, 'Log work', pos=(10, 110))
        self.log_btn.Enable(False)
        self.cancel_btn = wx.Button(self.panel, -1, 'Done', pos=(150, 110))
        
        #Bind events
        self.Bind(wx.EVT_CHOICE, self.projectSelected, self.proj_choice)
        self.Bind(wx.EVT_BUTTON, self.backDate, self.log_btn)
        self.Bind(wx.EVT_BUTTON, self.close, self.cancel_btn)
        
        for x in xrange(len(projectList)):
            if projectList[x] == projectName:
                self.proj_choice.SetSelection(x)
                self.projectSelected(None)
                break
        
################################################################################

    def backDate(self, event): #Check date is valid then write to file
        #Get date from the picker
        date = self.datePicker.GetValue()
        dateArray = [date.GetDay(), date.GetMonth() + 1, date.GetYear()]
        
        workTime = (self.hours.GetValue() +
                    (float(self.mins.GetValue())/60)
                    )
        
        if workTime > 0:
            name = self.proj_choice.GetStringSelection()
            # Get backdate type
            result = self.logic.getBackdateType(name, dateArray, workTime)
    
            if result == self.logic.BackdateType.UNIQUE:
                self.logic.insertBackdate(name, dateArray, workTime)
                dlg = wx.MessageDialog(self, 'Successfully backdated',
                                       'Success', wx.OK
                                       )
                dlg.ShowModal()
                self.parent.showProjectInfoInTable(name)
                
            elif result == self.logic.BackdateType.HAS_ENTRY:
                prevHours = self.logic.getHoursOnDate(name, dateArray)
                prevHr = int(prevHours)
                prevMin = int(round((prevHours - prevHr) * 60))
                hr = int(workTime)
                mins = int(round((workTime - hr) * 60))
                
                #Check if user wants to add on to time already recorded
                dlg = wx.MessageDialog(self, ('%02d/%02d/%d already has %d:%02d' +
                                              ' logged.\n\nAre you ' +
                                              'sure you want to log a ' +
                                              'further %d:%02d?'
                                              )
                                       %(dateArray[0], dateArray[1], dateArray[2], prevHr, prevMin, hr, mins),
                                       'Are you sure?', wx.YES_NO
                                       )
                result = dlg.ShowModal()
                if result == wx.ID_YES:
                    self.logic.insertBackdate(name, date, workTime)
                    self.parent.showProjectInfoInTable(name)
                    
            elif result == self.logic.BackdateType.SPILL_OVER:
                prevHours = self.logic.getHoursOnDate(name, dateArray)
                prevHr = int(prevHours)
                prevMin = int(round((prevHours - prevHr) * 60))
                dlg = wx.MessageDialog(self, ('%02d/%02d/%d already has %d:%02d' +
                                              'hrs logged.\n\nYou cannot ' +
                                              'log more than 24 hours on ' +
                                              'a single day.'
                                              )
                                       %(dateArray[0], dateArray[1], dateArray[2], prevHr, prevMin),
                                       'Invalid time', wx.OK
                                       )
                result = dlg.ShowModal()
                
            elif result == self.logic.BackdateType.FUTURE:
                dlg = wx.MessageDialog(self,
                                       'Please choose a date today or earlier.',
                                       'Invalid date selection', wx.OK
                                       )
                dlg.ShowModal()
                
            else:
                dlg = wx.MessageDialog(self,
                                       'Oops! Something went wrong',
                                       'Error', wx.OK
                                       )
                dlg.ShowModal()
        else:
            #Tell user to input valid time
            dlg2 = wx.MessageDialog(self, 'Please add a time longer than 0:00',
                                    'Invalid time',
                                    wx.OK | wx.ICON_INFORMATION
                                    )
            dlg2.ShowModal()
        
################################################################################

    def close(self, event):
        self.Destroy()
        
################################################################################

    def projectSelected(self, event): #Enable backdate button
        self.log_btn.Enable(True)
        
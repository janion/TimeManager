# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 15:02:44 2015

@author: erik_
"""

import wx
import datetime as dt
import csv
import os

class NewProjectDlg(wx.Dialog):
    def __init__(self, parent, idd, logic):
        wx.Dialog.__init__(self, parent, idd, 'New Project', size=(250, 170))
        self.parent = parent
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
        self.date = wx.GenericDatePickerCtrl(self.panel, size=(100, -1),
                                             pos=(10, 80)
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
        self.Bind(wx.EVT_TEXT, self.ProjectSelected, self.proj_name)
        self.Bind(wx.EVT_BUTTON, self.SaveProject, self.save_btn)
        self.Bind(wx.EVT_BUTTON, self.Close, self.cancel_btn)
        
################################################################################

    def Close(self, event):
        self.Destroy()
        
################################################################################

    def ProjectSelected(self, event): #Enable/disable save button as appropriate
        if self.proj_name.GetValue().strip(' ') != '':
            self.save_btn.Enable(True)
        else:
            self.save_btn.Enable(False)
        
################################################################################

    def SaveProject(self, event): #Create project file if name is unique
        if self.proj_name.GetValue() not in self.logic.getProjectNames():
            #If project name is unique
        
            #Get project name, number of hours entered and start date
            name = self.proj_name.GetValue()
            work_time = round(self.hours.GetValue() +
                              float(self.mins.GetValue()) / 60, 2
                              )

            date = str(self.date.GetValue())[:8].split('/')
            date[2] = int('20' + date[2])
            temp = int(date[1])
            date[1] = int(date[0])
            date[0] = temp
        
            #Get today's date
            today = dt.date.today().strftime("%d-%m-%Y").split('-')
            today = [int(today[0]), int(today[1]), int(today[2])]
                
            #Check date is today or earlier
            if ((date[2] < today[2]) or
                (date[2] == today[2] and date[1] < today[1]) or
                (date[2] == today[2] and date[1] == today[1] and
                 date[0] <= today[0])
                ):
                    self.logic.createNewProjectFile(name, date, work_time)
                    #Add to list ctrl on main window
                    self.parent.getProjectInfo(name)
                    self.Destroy()
            else:
                #Inform user of invalid date
                dlg = wx.MessageDialog(self,
                                       'Please choose a date today or earlier.',
                                       'Invalid date selection', wx.OK
                                       )
                dlg.ShowModal()
                dlg.Destroy()
        else:
            #Tell user to enter another name
            dlg2 = wx.MessageDialog(
                self, 'That project name is already in use',
                'Invalid project name', wx.OK | wx.ICON_INFORMATION
                )
            dlg2.ShowModal()
            dlg2.Destroy()
        
        
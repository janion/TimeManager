# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 15:00:48 2015

@author: erik_
"""

import wx
import time

class WorkSessionDlg(wx.Dialog):
    def __init__(self, parent, idd, logic, index = -1):        
        wx.Dialog.__init__(self, parent, idd, 'Work session', size=(250, 140))
        self.parent = parent
        self.panel = wx.Panel(self, -1)
        
        self.logic = logic
        
        #Create text and choice box for the project to work on
        wx.StaticText(self.panel, -1, "Please select the project to work on:",
                      (10, 10)
                      )
        self.proj_choice = wx.Choice(self.panel, pos=(10, 30), size=(225, -1),
                                     choices=self.logic.getProjectNames()
                                     )
        #Create timer label
        self.timer_text = wx.StaticText(self.panel, -1,
                                        "Current work session: 00:00:00",
                                        (10, 60)
                                        )
        
        #Create buttons
        self.start_btn = wx.Button(self.panel, -1, 'Start Session', pos=(10, 80)
                                   )
        self.start_btn.Enable(False)
        self.stop_btn = wx.Button(self.panel, -1, 'End Session', pos=(150, 80))
        self.stop_btn.Enable(False)
        
        #Bind events
        self.Bind(wx.EVT_CHOICE, self.ProjectSelected, self.proj_choice)
        self.Bind(wx.EVT_BUTTON, self.StartSesh, self.start_btn)
        self.Bind(wx.EVT_BUTTON, self.EndSesh, self.stop_btn)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        
        self.Bind(wx.EVT_TIMER, self.OnTimer)
        
        if index != -1:
            self.proj_choice.SetSelection(index)
            self.ProjectSelected(None)

################################################################################

    def EndSesh(self, event): #Stop timer and save session
        self.end_time = time.time()
        self.timer.Stop()
        del self.timer
        
        #Enable/disable the appropriate buttons
        self.proj_choice.Enable(True)
        self.start_btn.Enable(True)
        self.stop_btn.Enable(False)
        self.timer_text.Label = 'Current work session: 00:00:00'
        name = self.proj_choice.GetStringSelection()
        
        workHours = round((self.end_time - self.start_time) / 3600., 2)
        self.logic.recordSession(name, workHours)
                    
        #Update list ctrl in main window
        if self.end_time != self.start_time:
            self.parent.getProjectInfo(name)

################################################################################

    def OnClose(self, event): #Prevent user from closing an active session
        if self.proj_choice.Enabled == False:
            #Choice box only disabled if session is active
            dlg = wx.MessageDialog(self, 'Work session in progress\n\n'\
                                'Please finish session before exiting',
                                'Unfinished work session', wx.OK
                                )
            dlg.ShowModal()
        else:
            event.Skip()

################################################################################

    def OnTimer(self, event): #Update timer label when triggered (every second)
        #Get current time
        duration = (self.timer_text.GetLabel()
                    .strip('Current work session: ')
                    .split(':')
                    )
        
        if duration[2] != '59': #Not minute tick over
            if int(duration[2]) < 9: #Add leading zero for seconds under ten
                duration[2] = '0' + str(int(duration[2]) + 1)
            else:
                duration[2] = str(int(duration[2]) + 1)
                
        elif duration[1] != '59': #Minute tick over but not hour tick over
            duration[2] = '00'
            if int(duration[1]) < 9: #Add leading zero for minutes under ten
                duration[1] = '0' + str(int(duration[1]) + 1)
            else:
                duration[1] = str(int(duration[1]) + 1)
                
        else: #Hour tick over
            (duration[2],duration[1]) = ('00', '00')
            if int(duration[0]) < 9: #Add leadinf=g zero for hours under ten
                duration[0] = '0' + str(int(duration[0]) + 1)
            else:
                duration[0] = str(int(duration[0]) + 1)
                
        #Update timer label
        self.timer_text.Label = ('Current work session: %s:%s:%s'
                                 %tuple(duration)
                                 )
        
################################################################################

    def ProjectSelected(self, event): #Enable start button when project selected
        self.start_btn.Enable(True)

################################################################################

    def StartSesh(self, event): #Disable/enable buttos and start the timer
        self.proj_choice.Enable(False)
        self.start_btn.Enable(False)
        self.stop_btn.Enable(True)
        self.start_time = time.time()
        
        self.timer = wx.Timer(self)
        self.timer.Start(1000)
            
            
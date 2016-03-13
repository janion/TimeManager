# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 15:00:48 2015

@author: erik_
"""

import wx
import csv
import datetime as dt
import time

class WorkSessionDlg(wx.Dialog):
    def __init__(self, parent, id, title, projects):
        wx.Dialog.__init__(self, parent, id, title, size=(250, 140))
        self.parent = parent
        self.panel = wx.Panel(self, -1)
        
        #Create text and choice box for the project to work on
        wx.StaticText(self.panel, -1, "Please select the project to work on:",
                      (10, 10)
                      )
        self.proj_choice = wx.Choice(self.panel, pos=(10, 30), size=(225, -1),
                                     choices=projects
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
        
        #Find hours worked in decimal
        hours_worked = round((self.end_time - self.start_time) / 3600., 2)      
        
        if hours_worked > 0.00: #If a non-zero amount of time has been worked
            #Get name of project and today's date
            name = self.proj_choice.GetStringSelection()
            today = dt.date.today().strftime("%d-%m-%Y").split('-')
            today = [int(today[0]), int(today[1]), int(today[2])]
    
            #Read csv file
            with open('Project_man_%s.csv' %name, 'rb') as csvfile:
                r1 = csv.reader(csvfile, delimiter=',')
                
                (days, months, years, hours) = ([], [], [], [])
                #Gather data into lists
                for row in r1:
                    try:
                        hours.append(float(row[3]))
                        years.append(int(row[2]))
                        months.append(int(row[1]))
                        days.append(int(row[0]))
                    except:
                        pass #Ignore erroneous entries
            
            if [days[-1], months[-1], years[-1]] == today:
                #Update last entry if it has today's date
                hours[-1] += hours_worked
            else:
                #Else make a new entry on the end
                days.append(today[0])
                months.append(today[1])
                years.append(today[2])
                hours.append(hours_worked)
                
            #Write to csv file
            with open('Project_man_%s.csv' %name, 'rb+') as csvfile:
                csvfile.truncate() #Part of the bodge a few lines above
                w1 = csv.writer(csvfile, delimiter=',')
                for x in xrange(len(hours)):
                    w1.writerow([days[x], months[x], years[x], hours[x]])
                    
            #Update list ctrl in main window
            self.parent.GetProjectInfo(name)
            
            
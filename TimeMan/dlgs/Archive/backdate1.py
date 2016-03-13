# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 14:59:28 2015

@author: erik_
"""

import wx
import csv
import datetime as dt

class BackDateDlg(wx.Dialog):
    def __init__(self, parent, id, title, projects):
        wx.Dialog.__init__(self, parent, id, title, size=(250, 170))
        self.parent = parent
        self.panel = wx.Panel(self, -1)
        
        #Create text and project choice box
        wx.StaticText(self.panel, -1,
                      "Please select the project to back date:", (10, 10)
                      )
        self.proj_choice = wx.Choice(self.panel, pos=(10, 30), size=(225, -1),
                                     choices=projects
                                     )
        #Create text and date picker
        wx.StaticText(self.panel, -1, "Select date:", (10, 60))
        self.date = wx.GenericDatePickerCtrl(self.panel, size=(100, -1),
                                             pos=(10, 80)
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
        self.Bind(wx.EVT_CHOICE, self.ProjectSelected, self.proj_choice)
        self.Bind(wx.EVT_BUTTON, self.BackDate, self.log_btn)
        self.Bind(wx.EVT_BUTTON, self.Close, self.cancel_btn)
        
################################################################################

    def ReadFile(self, name): #Find all the entries in a file
        with open('Project_man_%s.csv' %name, 'rb') as csvfile:
            r1 = csv.reader(csvfile, delimiter=',')
            
            #Declare empty lists
            (days, months, years, hours) = ([], [], [], [])
            #Find the dates and hours worked
            for row in r1:
                try:
                    hours.append(float(row[3]))
                    years.append(int(row[2]))
                    months.append(int(row[1]))
                    days.append(int(row[0]))
                except:
                    pass #Skip an erroneous entry
            
        return (days, months, years, hours)
        
################################################################################

    def BackDate(self, event): #Check date is valid then write to file
        #Get date from the picker and convert to British format
        date = str(self.date.GetValue())[:8].split('/')
        date[2] = int('20' + date[2])
        temp = int(date[1])
        date[1] = int(date[0])
        date[0] = temp
        
        #Find today's date
        today = dt.date.today().strftime("%d-%m-%Y").split('-')
        today = [int(today[0]), int(today[1]), int(today[2])]
            
        #Check date is today or earlier
        if ((date[2] < today[2]) or
            (date[2] == today[2] and date[1] < today[1]) or
            (date[2] == today[2] and date[1] == today[1] and
             date[0] <= today[0])
            ):
            #Get project name
            name = self.proj_choice.GetStringSelection()
            #get data from the csv file
            (days, months, years, hours) = self.ReadFile(name)
            
            #Cehck if the backdate is earlier than all other entries
            if ((date[2] < years[0]) or
                (date[2] == years[0] and date[1] < months[0]) or
                (date[2] == years[0] and date[1] == months[0] and
                 date[0] < days[0])
                ):
                (minn, maxx) = (-1, 0)
            else:
                minn = -1
                maxx = len(years)
                #Find range of year
                for x in xrange(len(years)):
                    if years[x] < date[2]:
                        minn = x
                    if years[x] > date[2]:
                        maxx = x
                        break
                    
                #Find range of months
                for x in xrange(minn + 1, maxx):
                    if months[x] < date[1]:
                        minn = x
                    if months[x] > date[1]:
                        maxx = x
                        break
                    
                #Find range of days
                for x in xrange(minn + 1, maxx):
                    if days[x] < date[0]:
                        minn = x
                    if days[x] > date[0]:
                        maxx = x
                        break
            
            #Write date to the file
            self.InsertBackDate(name, date, days, months, years, hours, maxx,
                                maxx - minn
                                )
        else: #Tell user that date choice is invalid
            dlg = wx.MessageDialog(self,
                                   'Please choose a date today or earlier.',
                                   'Invalid date selection', wx.OK
                                   )
            dlg.ShowModal()
            
################################################################################

    def InsertBackDate(self, name, date, days, mths, yrs, hrs,index, delta):
        #Write data to file
    
        #Get hours to be backdated
        work_time = (self.hours.GetValue() +
                     (float(self.mins.GetValue())/60)
                     )
        
        if work_time > 0.00: #Check the time entered is valid
            update = True #Marker
            if delta == 1: #Delta == 1 means that it is a unique entry
                days.insert(index, date[0])
                mths.insert(index, date[1])
                yrs.insert(index, date[2])
                hrs.insert(index, round(work_time, 2))
            elif delta == 2: #Means that another entry must be updated
                if hrs[index - 1] != 0.00:
                #Check if user wants to add on to time already recorded
                    dlg = wx.MessageDialog(self, ('%d/%d/%d already has %4.2f' +
                                                  'hrs logged.\n\nAre you ' +
                                                  'sure you want to log a ' +
                                                  'further %4.2fhrs?'
                                                  )
                                           %tuple(date +
                                                  [hrs[index-1], work_time]
                                                  ),
                                           'Are you sure?', wx.YES_NO
                                           )
                    result = dlg.ShowModal()
                    if result == wx.ID_YES:
                        hrs[index-1] = round(hrs[index-1] + work_time, 2)
                    else:
                        update = False
                else:
                    hrs[index-1] = round(work_time, 2)
            
            if update == True:
                with open('Project_man_%s.csv' %name, 'rb+') as csvfile:
                    csvfile.truncate()
                    w1 = csv.writer(csvfile, delimiter=',')
                    
                    #Write the dates
                    for x in xrange(len(hrs)):
                        w1.writerow([days[x], mths[x], yrs[x], hrs[x]])
                
                self.parent.GetProjectInfo(name)
                #Tell user of success
                dlg2 = wx.MessageDialog(self,'Successfully backdated: %s'
                                        %name, 'Back date successful',
                                        wx.OK | wx.ICON_INFORMATION
                                        )
                dlg2.ShowModal()
        else:
            #Tell user to input valid time
            dlg2 = wx.MessageDialog(self, 'Please add a time longer than 0:00',
                                    'Invalid time',
                                    wx.OK | wx.ICON_INFORMATION
                                    )
            dlg2.ShowModal()
        
################################################################################

    def ProjectSelected(self, event):
        self.log_btn.Enable(True)
        
################################################################################

    def Close(self, event):
        self.Destroy()
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 14:59:28 2015

@author: erik_
"""

# Need InsertBackDate() method factoring into logic

import wx
import csv

class BackdateDlg(wx.Dialog):
    def __init__(self, parent, idd, logic):
        
        self.logic = logic
        
        wx.Dialog.__init__(self, parent, idd, 'Back date project', size=(250, 170))
        self.parent = parent
        self.panel = wx.Panel(self, -1)
        
        #Create text and project choice box
        wx.StaticText(self.panel, -1,
                      "Please select the project to back date:", (10, 10)
                      )
        self.proj_choice = wx.Choice(self.panel, pos=(10, 30), size=(225, -1),
                                     choices=self.logic.getProjectNames()
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

    def BackDate(self, event): #Check date is valid then write to file
        #Get date from the picker and convert to British format
        date = str(self.date.GetValue())[:8].split('/')
        date[2] = int('20' + date[2])
        temp = int(date[1])
        date[1] = int(date[0])
        date[0] = temp
        
        #Get project name
        name = self.proj_choice.GetStringSelection()
        # Get backdate data
        result = self.logic.backdate(date, name)

        if result[0]: #Tell user that date choice is invalid
            data = result[1]
            extent = result[2]
            #Write date to the file
            self.InsertBackDate(name, date, data[0], data[1], data[2], data[3], extent[0],
                                extent[1]
                                )
        else:
            dlg = wx.MessageDialog(self,
                                   'Please choose a date today or earlier.',
                                   'Invalid date selection', wx.OK
                                   )
            dlg.ShowModal()
        
################################################################################

    def Close(self, event):
        self.Destroy()
            
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
                #Insert entry into the lists
                days.insert(index, date[0])
                mths.insert(index, date[1])
                yrs.insert(index, date[2])
                hrs.insert(index, round(work_time, 2))
            elif delta == 2: #Means that another entry must be updated
                if (hrs[index - 1] + work_time) > 24: #Check if time is valid
                    #Tell user that the time is invalid
                    dlg = wx.MessageDialog(self, ('%d/%d/%d already has %4.2f' +
                                                  'hrs logged.\n\nYou cannot ' +
                                                  'log more than 24 hours on ' +
                                                  'a single day.'
                                                  )
                                           %tuple(date + [hrs[index-1]]),
                                           'Invalid time', wx.OK
                                           )
                    result = dlg.ShowModal()
                    update = False
                    
                elif hrs[index - 1] != 0.00:
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
                else: #If entry currently has zero hours, add work_time
                    hrs[index-1] = round(work_time, 2)
            
            if update == True: #If all criteria met and user happy
                #Write data to file
                with open('Project_man_%s.csv' %name, 'rb+') as csvfile:
                    csvfile.truncate()
                    w1 = csv.writer(csvfile, delimiter=',')
                    
                    #Write the entries
                    for x in xrange(len(hrs)):
                        w1.writerow([days[x], mths[x], yrs[x], hrs[x]])
                
                #Update the list ctrl in main window
                self.parent.getProjectInfo(name)
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

    def ProjectSelected(self, event): #Enable backdate button
        self.log_btn.Enable(True)
        
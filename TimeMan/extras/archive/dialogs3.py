# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 12:38:12 2015

@author: Janion
"""

import wx
import csv
import datetime as dt
import time
import os
import matplotlib

##########
matplotlib.use('WXAgg')
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx as toolbar
##########
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

################################################################################

class DataWindow(wx.Frame):
    def __init__(self,parent,id,title):
        wx.Frame.__init__(self,parent,id,title,size=(890,470))#(285,320))#
        self.panel = wx.Panel(self,-1)
        
        self.data_list = wx.ListCtrl(self.panel,-1,pos=(10,10),size=(250,380),
                                     style=wx.LC_REPORT
                                     )
                                   
        buff = (self.data_list.GetPosition()[0] + 10 +
                self.data_list.GetSize()[0]
                )
        
        wx.StaticText(self.panel,-1,"",pos=(buff,10))

        self.zoom_btn = wx.ToggleButton(self.panel,-1,'Zoom',pos=(10,400),size=(70,-1))
        self.pan_btn = wx.ToggleButton(self.panel,-1,'Pan',pos=(90,400),size=(70,-1))
        self.home_btn = wx.Button(self.panel,-1,'Reset view',pos=(170,400),size=(70,-1))

        #Add columns
        self.data_list.InsertColumn(0, "Date", width=80)
        self.data_list.InsertColumn(1, "hours", width=60)
        self.data_list.InsertColumn(2, "Total hours", width=90)
        
        
        (days,months,years,hours,tot) = self.GetData(title)
        
        for x in xrange(len(days)):
            self.data_list.InsertStringItem(x,'%d/%d/%d'
                                            %(days[x],months[x],years[x])
                                            )
            self.data_list.SetStringItem(x, 1, ("%d:%2d" %(int(hours[x]), int(round((hours[x]%1)*60)))).replace(" ", "0"))
            self.data_list.SetStringItem(x, 2, str(tot[x]))
            
        self.MakeDates(days,months,years,hours,tot)
        self.PlotData()
        
        self.zoom_btn.Bind(wx.EVT_TOGGLEBUTTON,self.Zoom)
        self.pan_btn.Bind(wx.EVT_TOGGLEBUTTON,self.Pan)
        self.home_btn.Bind(wx.EVT_BUTTON,self.Home)

################################################################################

    def Zoom(self,event):
        self.toolbar.zoom()
        if self.pan_btn.GetValue() == True:
            self.pan_btn.SetValue(False)

################################################################################

    def Pan(self,event):
        self.toolbar.pan()
        if self.zoom_btn.GetValue() == True:
            self.zoom_btn.SetValue(False)

################################################################################

    def Home(self,event):
        self.toolbar.home()

################################################################################
    
    def PlotData(self):
        """
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))
#        plt.gca().xaxis.set_major_locator(mdates.DayLocator())
        plt.plot(self.dates,self.wk_hrs,'r.-')
        plt.gcf().autofmt_xdate()

        plt.ylim(0,max(self.wk_hrs)*1.1)       
        
        plt.show()
      
        
        """
        
        #Part of trying to graph work flow
        self.figure = plt.Figure()
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.axes = self.figure.add_subplot(111)
        
        self.axes.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))
#        plt.gca().xaxis.set_major_locator(mdates.DayLocator())
        self.figure.autofmt_xdate()
        self.axes.plot(self.dates,self.wk_hrs,'r.-')
#        self.axes.set_ylim(0,max(self.wk_hrs)*1.1)
#        self.axes.set_xlim(dt.date(2015,01,01),dt.date(2015,12,01))
        
        self.toolbar = toolbar(self.canvas)
        self.toolbar.Hide()
        
        
        self.Sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.Sizer.Add(self.panel, 0, wx.EXPAND)
        self.Sizer.Add(self.canvas, 0, wx.EXPAND, 8)

################################################################################
    
    def MakeDates(self,days,months,years,hours,tot):
            
        self.dates = []
        self.wk_hrs = []
        count = 0

        for year in xrange(min(years),int(dt.date.today().strftime('%Y'))+1):
            for month in xrange(1,13):
                for day in xrange(1,31):
                    
                    #Provided that the dates are withing the range of start to end months
                    if not ((year == years[0] and month < months[0]) or
                            (year == years[-1] and month > months[-1])
                            ):
                    
                        if (day,month,year) not in zip(days,months,years):
                            try:
                                self.dates.append(dt.date(year,month,day))
                                self.wk_hrs.append(0.0)
                            except:
                                1==1
                        else:
                            self.dates.append(dt.date(year,month,day))
                            self.wk_hrs.append(hours[count])
                            count += 1


################################################################################
    
    def GetData(self, filename):
        with open('Project_man_%s.csv' %filename,'rb') as csvfile:
            r1 = csv.reader(csvfile,delimiter=',')
            
            (days,months,years,hours,tot) = ([],[],[],[],[])
            for row in r1:
                try:
                    hours.append(float(row[3]))
                    days.append(int(row[0]))
                    months.append(int(row[1]))
                    years.append(int(row[2]))
                    try:
                        tot.append(tot[-1]+float(row[3]))
                    except:
                        tot.append(float(row[3]))
                except:
                    pass
        
        return (days,months,years,hours,tot)

################################################################################
################################################################################

class BackDateDlg(wx.Dialog):
    def __init__(self,parent,id,title,projects):
        wx.Dialog.__init__(self,parent,id,title,size=(250,170))
        self.parent = parent
        self.panel = wx.Panel(self,-1)
        
        wx.StaticText(self.panel,-1,"Please select the project to back date:",
                      (10, 10)
                      )
        self.proj_choice = wx.Choice(self.panel,pos=(10,30),size=(225,-1),
                                     choices=projects
                                     )
        wx.StaticText(self.panel,-1,"Select date:",(10,60))
        self.date = wx.GenericDatePickerCtrl(self.panel, size=(100,-1),
                                             pos=(10,80)
                                             )
                                             
        wx.StaticText(self.panel,-1,"Hours:",(120,60))
        self.hours = wx.SpinCtrl(self.panel, -1, "", pos=(120,80),size=(40,-1))
        self.hours.SetRange(0,23)
        self.hours.SetValue(0)
        
        wx.StaticText(self.panel,-1,"Minutes:",(170,60))
        self.mins = wx.SpinCtrl(self.panel, -1, "", pos=(170,80),size=(40,-1))
        self.mins.SetRange(0,59)
        self.mins.SetValue(0)
        
        self.log_btn = wx.Button(self.panel,-1,'Log work',pos=(10,110))
        self.log_btn.Enable(False)
        self.cancel_btn = wx.Button(self.panel,-1,'Done',pos=(150,110))
        
        self.Bind(wx.EVT_CHOICE,self.ProjectSelected,self.proj_choice)
        self.Bind(wx.EVT_BUTTON,self.BackDate,self.log_btn)
        self.Bind(wx.EVT_BUTTON,self.Close,self.cancel_btn)
        
################################################################################

    def ReadFile(self,name):
        with open('Project_man_%s.csv' %name, 'rb') as csvfile:
            r1 = csv.reader(csvfile,delimiter=',')
            
            days = []
            months = []
            years = []
            hours = []
            #Find the dates
            for row in r1:
                try:
                    hours.append(float(row[3]))
                    years.append(int(row[2]))
                    months.append(int(row[1]))
                    days.append(int(row[0]))
                except:
                    1==1#Part of the bodge
            
        return (days, months, years, hours)
        
################################################################################

    def BackDate(self,event):
        date = str(self.date.GetValue())[:8].split('/')
        date[2] = int('20'+date[2])
        temp = int(date[1])
        date[1] = int(date[0])
        date[0] = temp
        
### Make date today or earlier
        today = dt.date.today().strftime("%d-%m-%Y").split('-')
        today = [int(today[0]),int(today[1]),int(today[2])]
            
        if ((date[2] < today[2]) or
            (date[2] == today[2] and date[1] < today[1]) or
            (date[2] == today[2] and date[1] == today[1] and date[0] <= today[0])
            ):
### /Make date today or earlier
        
            worked_time = self.hours.GetValue() + (float(self.mins.GetValue())/60)
            
            name = self.proj_choice.GetStringSelection()
            #Look in the csv file
            (days, months, years, hours) = self.ReadFile(name)
            
            if ((date[2] < years[0]) or
                (date[2] == years[0] and date[1] < months[0]) or
                (date[2] == years[0] and date[1] == months[0] and date[0] < days[0])
                ):
                (minn, maxx) = (-1,0)
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
                for x in xrange(minn+1,maxx):
                    if months[x] < date[1]:
                        minn = x
                    if months[x] > date[1]:
                        maxx = x
                        break
                    
                #Find range of days
                for x in xrange(minn+1,maxx):
                    if days[x] < date[0]:
                        minn = x
                    if days[x] > date[0]:
                        maxx = x
                        break
            
            self.InsertBackDate(name,date,days,months,years,hours,
                                worked_time,maxx,maxx-minn
                                )
        else:
            dlg = wx.MessageDialog(self,
                                   'Please choose a date today or earlier.',
                                   'Invalid date selection', wx.OK
                                   )
            dlg.ShowModal()
            
        
        
################################################################################

    def InsertBackDate(self,name,date,days,mths,yrs,hrs,work_time,maxx,delta):
        
        if work_time > 0.00:
            update = True
            if delta == 1:
                days.insert(maxx,date[0])
                mths.insert(maxx,date[1])
                yrs.insert(maxx,date[2])
                hrs.insert(maxx,round(work_time,2))
            elif delta == 2:
                if hrs[maxx-1] != 0.00:
                    dlg = wx.MessageDialog(self,'%d/%d/%d already has %4.2fhrs '\
                                           'logged.\n\nAre you sure you want to '\
                                           'log a further %4.2fhrs?'
                                           %tuple(date+[hrs[maxx-1],work_time]),
                                           'Are you sure?', wx.YES_NO
                                           )
                    result = dlg.ShowModal()
                    if result == wx.ID_YES:
                        hrs[maxx-1] = round(hrs[maxx-1] + work_time,2)
#                        hrs[maxx-1] += work_time
                    else:
                        update = False
                else:
                    update = True
            
            if update == True:
                with open('Project_man_%s.csv' %name, 'rb+') as csvfile:
                    csvfile.truncate()#Part of the bodge
                    w1 = csv.writer(csvfile,delimiter=',')
                    
                    #Write the dates
                    for x in xrange(len(hrs)):
                        w1.writerow([days[x],mths[x],yrs[x],hrs[x]])
                
                self.parent.GetProjectInfo(name)
                #Tell user of success
                dlg2 = wx.MessageDialog(self,'Successfully backdated: %s' %name,
                                        'Back date successful',
                                        wx.OK | wx.ICON_INFORMATION
                                        )
                dlg2.ShowModal()
        else:
            #Tell user to input valid time
            dlg2 = wx.MessageDialog(self,'Please add a time longer than 0:00',
                                    'Invalid time',
                                    wx.OK | wx.ICON_INFORMATION
                                    )
            dlg2.ShowModal()
        
        
################################################################################

    def ProjectSelected(self,event):
        self.log_btn.Enable(True)
        
################################################################################

    def Close(self,event):
        self.Destroy()

################################################################################
################################################################################

class WorkSessionDlg(wx.Dialog):
    def __init__(self,parent,id,title,projects):
        wx.Dialog.__init__(self,parent,id,title,size=(250,140))
        self.parent = parent
        self.panel = wx.Panel(self,-1)
        
        wx.StaticText(self.panel,-1,"Please select the project to work on:",
                      (10, 10)
                      )
        self.proj_choice = wx.Choice(self.panel,pos=(10,30),size=(225,-1),
                                     choices=projects
                                     )
        self.timer_text = wx.StaticText(self.panel,-1,
                                        "Current work session: 00:00:00",
                                        (10,60)
                                        )
        
        self.start_btn = wx.Button(self.panel,-1,'Start Session',pos=(10,80))
        self.start_btn.Enable(False)
        self.stop_btn = wx.Button(self.panel,-1,'End Session',pos=(150,80))
        self.stop_btn.Enable(False)
        
        self.Bind(wx.EVT_CHOICE,self.ProjectSelected,self.proj_choice)
        self.Bind(wx.EVT_BUTTON,self.StartSesh,self.start_btn)
        self.Bind(wx.EVT_BUTTON,self.EndSesh,self.stop_btn)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        
        self.Bind(wx.EVT_TIMER, self.OnTimer)

################################################################################

    def OnClose(self, event):
        if self.proj_choice.Enabled == False:
            dlg = wx.MessageDialog(self,'Work session in progress\n\n'\
                                'Please finish session before exiting',
                                'Unfinished work session', wx.OK
                                )
            dlg.ShowModal()
        else:
            event.Skip()

################################################################################

    def OnTimer(self, event):
        duration = self.timer_text.GetLabel().strip('Current work session: ').split(':')
        if duration[2] != '59':
            if int(duration[2]) < 9:
                duration[2] = '0' + str(int(duration[2]) + 1)
            else:
                duration[2] = str(int(duration[2]) + 1)
        elif duration[1] != '59':
            duration[2] = '00'
            if int(duration[1]) < 9:
                duration[1] = '0' + str(int(duration[1]) + 1)
            else:
                duration[1] = str(int(duration[1]) + 1)
        else:
            (duration[2],duration[1]) = ('00','00')
            if int(duration[0]) < 9:
                duration[0] = '0' + str(int(duration[0]) + 1)
            else:
                duration[0] = str(int(duration[0]) + 1)
        self.timer_text.Label = 'Current work session: %s:%s:%s' %tuple(duration)
        
################################################################################

    def ProjectSelected(self,event):
        self.start_btn.Enable(True)

################################################################################

    def StartSesh(self,event):
        self.proj_choice.Enable(False)
        self.start_btn.Enable(False)
        self.stop_btn.Enable(True)
        self.start_time = time.time()
        
        self.timer = wx.Timer(self)
        self.timer.Start(1000)

################################################################################

    def EndSesh(self,event):
        self.end_time = time.time()
        self.timer.Stop()
        del self.timer
        
        self.proj_choice.Enable(True)
        self.start_btn.Enable(True)
        self.stop_btn.Enable(False)
        self.timer_text.Label = 'Current work session: 00:00:00'
        
        hours_worked = round((self.end_time-self.start_time)/3600.,2)      
        
        if hours_worked > 0.00:
            name = self.proj_choice.GetStringSelection()
            today = dt.date.today().strftime("%d-%m-%Y").split('-')
            today = [int(today[0]),int(today[1]),int(today[2])]
    
            #Read csv file
            with open('Project_man_%s.csv' %name, 'rb') as csvfile:
                r1 = csv.reader(csvfile,delimiter=',')
                
                days = []
                months = []
                years = []
                hours = []
                #Find the dates
                for row in r1:
                    try:
                        hours.append(float(row[3]))
                        years.append(int(row[2]))
                        months.append(int(row[1]))
                        days.append(int(row[0]))
                    except:
                        1==1
                        #This is a bodge. Must be investigated later
            
            if [days[-1],months[-1],years[-1]] == today:
                hours[-1] += hours_worked
            else:
                days.append(today[0])
                months.append(today[1])
                years.append(today[2])
                hours.append(hours_worked)
            
#            os.system('Project_man_%s.csv' %name)
#            time.sleep(20)
                
            #Write to csv file
            with open('Project_man_%s.csv' %name,'rb+') as csvfile:
                csvfile.truncate() #Part of the bodge a few lines above
                w1 = csv.writer(csvfile,delimiter=',')
                for x in xrange(len(hours)):
                    w1.writerow([days[x],months[x],years[x],hours[x]])

#            os.system('Project_man_%s.csv' %name)
#            time.sleep(20)            
            
            pos = self.parent.proj_list.FindItem(-1,name)
            tot = self.parent.proj_list.GetItemText(pos,1)
            ths_wk = self.parent.proj_list.GetItemText(pos,2)
            
            self.parent.proj_list.SetStringItem(pos,1,str(hours_worked+float(tot)))
            self.parent.proj_list.SetStringItem(pos,2,str(hours_worked+float(ths_wk)))

################################################################################
################################################################################

class NewProjectDlg(wx.Dialog):
    def __init__(self,parent,id,title):
        wx.Dialog.__init__(self,parent,id,title,size=(250,170))
        self.parent = parent
        self.panel = wx.Panel(self,-1)
        
        wx.StaticText(self.panel,-1,"Please enter the name of the project:",
                      (10, 10)
                      )
        self.proj_name = wx.TextCtrl(self.panel,-1,'',pos=(10,30),size=(225,-1))
        wx.StaticText(self.panel,-1,"Select start date:",(10,60))
        self.date = wx.GenericDatePickerCtrl(self.panel, size=(100,-1),
                                             pos=(10,80)
                                             )
                                             
        wx.StaticText(self.panel,-1,"Hours:",(120,60))
        self.hours = wx.SpinCtrl(self.panel, -1, "", pos=(120,80),size=(40,-1))
        self.hours.SetRange(0,23)
        self.hours.SetValue(0)
        
        wx.StaticText(self.panel,-1,"Minutes:",(170,60))
        self.mins = wx.SpinCtrl(self.panel, -1, "", pos=(170,80),size=(40,-1))
        self.mins.SetRange(0,59)
        self.mins.SetValue(0)
        
        self.save_btn = wx.Button(self.panel,-1,'Save',pos=(10,110))
        self.save_btn.Enable(False)
        self.cancel_btn = wx.Button(self.panel,-1,'Cancel',pos=(150,110))
        
        self.Bind(wx.EVT_TEXT,self.ProjectSelected,self.proj_name)
        self.Bind(wx.EVT_BUTTON,self.SaveProject,self.save_btn)
        self.Bind(wx.EVT_BUTTON,self.Close,self.cancel_btn)
        
################################################################################

    def SaveProject(self,event):
        #If project name is original
        if self.proj_name.GetValue() not in self.parent.projects:
            name = self.proj_name.GetValue()
            work_time = round(self.hours.GetValue() +
                              float(self.mins.GetValue())/60,2
                              )
            date = str(self.date.GetValue())[:8].split('/')
            date[2] = int('20'+date[2])
            temp = int(date[1])
            date[1] = int(date[0])
            date[0] = temp
        
    ### Make date today or earlier
            today = dt.date.today().strftime("%d-%m-%Y").split('-')
            today = [int(today[0]),int(today[1]),int(today[2])]
                
            if ((date[2] < today[2]) or
                (date[2] == today[2] and date[1] < today[1]) or
                (date[2] == today[2] and date[1] == today[1] and date[0] <= today[0])
                ):
    ### /Make date today or earlier
                                      
                    #Create csv file for project
                    with open('Project_man_%s.csv' %name,'wb') as csvfile:
                              w1 = csv.writer(csvfile,delimiter=',')
                              w1.writerow(date+['%f' %work_time])
                    #Make file hidden
                    os.popen('attrib +h Project_man_%s.csv' %name)
                    self.parent.projects.append(name)
                    self.parent.GetProjectInfo(name)
                    self.Destroy()
            else:
                dlg = wx.MessageDialog(self,
                                       'Please choose a date today or earlier.',
                                       'Invalid date selection', wx.OK
                                       )
                dlg.ShowModal()
        else:
            #Tell user to find other name
            dlg2 = wx.MessageDialog(self,'That project name is already in use',
                                    'Invalid project name',
                                    wx.OK | wx.ICON_INFORMATION
                                    )
            dlg2.ShowModal()
            dlg2.Destroy()
        
################################################################################

    def ProjectSelected(self,event):
        if self.proj_name.GetValue().strip(' ') != '':
            self.save_btn.Enable(True)
        else:
            self.save_btn.Enable(False)
        
################################################################################

    def Close(self,event):
        self.Destroy()
                    
################################################################################
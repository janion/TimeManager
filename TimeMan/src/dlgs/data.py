# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 14:56:36 2015

@author: erik_
"""

import wx
import csv
import datetime as dt

import config

class DataWindow(wx.Frame):
    
    def __init__(self, parent, idd, title):
        wx.Frame.__init__(self, parent, idd, title, size=(270, 440))
        self.panel = wx.Panel(self, -1)
        
        #Open list ctrl to house data
        self.data_list = wx.ListCtrl(self.panel, -1, pos=(10, 10),
                                     size=(230, 380), style=wx.LC_REPORT
                                     )

        #Add columns
        self.data_list.InsertColumn(0, "Date", width=80)
        self.data_list.InsertColumn(1, "hours", width=60)
        self.data_list.InsertColumn(2, "Total hours", width=90)
        
        
        (days, months, years, hours, tot) = self.GetData(title)
        
        for x in xrange(len(days)):
            self.data_list.InsertStringItem(x, '%d/%d/%d'
                                            %(days[x], months[x], years[x])
                                            )
            self.data_list.SetStringItem(
                x, 1,("%d:%2d" %(int(hours[x]), int(round((hours[x]%1)*60))))
                .replace(" ", "0")
                )
            self.data_list.SetStringItem(
                x, 2, ("%d:%2d" %(int(tot[x]), int(round((tot[x]%1)*60))))
                .replace(" ", "0")
                )

        if config.hasGraphs:
            
            self.SetSize((870, 470))
            
            #Create buttons for graph manipulation
            self.zoom_btn = wx.ToggleButton(self.panel, -1, 'Zoom', pos=(10, 400),
                                            size=(70, -1)
                                            )
            self.pan_btn = wx.ToggleButton(self.panel, -1, 'Pan', pos=(90, 400),
                                           size=(70, -1)
                                           )
            self.home_btn = wx.Button(self.panel, -1, 'Reset view', pos=(170, 400),
                                      size=(70, -1)
                                      )
                    
            #This is to ensure there is a sufficient border on RHS
            buff = (self.data_list.GetPosition()[0] + 10 +
                    self.data_list.GetSize()[0]
                    )
            wx.StaticText(self.panel, -1, "", pos=(buff, 10))
                
            #Make data into 2 lists:
                #one of all dates in range
                #one of all worked hours (including zeros)
            self.MakeDates(days, months, years, hours, tot)
            self.PlotData()
            
            #Bind events
            self.zoom_btn.Bind(wx.EVT_TOGGLEBUTTON, self.Zoom)
            self.pan_btn.Bind(wx.EVT_TOGGLEBUTTON, self.Pan)
            self.home_btn.Bind(wx.EVT_BUTTON, self.Home)

################################################################################
    
    def GetData(self, filename): #Extract data from .csv file
        with open('Project_man_%s.csv' %filename, 'rb') as csvfile:
            r1 = csv.reader(csvfile, delimiter=',')
            
            #Declare empty lists
            (days, months, years, hours, tot) = ([], [], [], [], [])
            for row in r1:
                try: #Append data to lists
                    hours.append(float(row[3]))
                    days.append(int(row[0]))
                    months.append(int(row[1]))
                    years.append(int(row[2]))
                    try:
                        tot.append(tot[-1] + float(row[3]))
                    except:
                        tot.append(float(row[3]))
                except:
                    pass #Skip erroneous entries
        
        return (days, months, years, hours, tot)

################################################################################
    
    def MakeDates(self, days, months, years, hours, tot): #Make list of dates
    #in range as well as a list of the hours worked on each day.
            
        self.dates = []
        self.wk_hrs = []
        count = 0

        for year in xrange(min(years), dt.date.today().year + 1):
            #For years in range
            for month in xrange(1, 13): #For month in each year
                for day in xrange(1, 32): #For day in each month
                    
                    #Provided that the dates are within the range of start to end months
                    if not ((year == years[0] and month < months[0]) or
                            (year == years[-1] and month > months[-1])
                            ):
                    
                        if (day,month,year) not in zip(days, months, years):
                            try: #Add date with zero hours if not recorded
                                self.dates.append(dt.date(year, month, day))
                                self.wk_hrs.append(0.0)
                            except:#Skip dates which do not exist
                                pass
                        else: #Add hours worked if date is recorded
                            self.dates.append(dt.date(year, month, day))
                            self.wk_hrs.append(hours[count])
                            count += 1
                            #zip(days, months, years).index((day, month, year))

################################################################################

    def Home(self, event): #Reset graph view
        self.toolbar.home()

################################################################################

    def Pan(self, event): #Enable panning and disable zoom button
        self.toolbar.pan()
        if self.zoom_btn.GetValue() == True:
            self.zoom_btn.SetValue(False)

################################################################################

    def Zoom(self, event): #Enable zooming and deslect the pan button
        self.toolbar.zoom()
        if self.pan_btn.GetValue() == True:
            self.pan_btn.SetValue(False)

################################################################################
    
    def PlotData(self): #Create graph object and embed it and the panel into
    #the dialog
    
    
        import matplotlib
        ##########
        matplotlib.use('WXAgg')
        from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
        from matplotlib.backends.backend_wx import NavigationToolbar2Wx as toolbar
        ##########
        import matplotlib.pyplot as plt
        import matplotlib.dates as mdates
    
    
    
        #Create figure
        self.figure = plt.Figure()
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.axes = self.figure.add_subplot(111)
        
        #Add dates as x axis
        self.axes.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))
        self.figure.autofmt_xdate()
        #Plot data
        self.axes.plot(self.dates,self.wk_hrs,'r.-')
        
        #Create figure toolbar to allow user to manipulate graph
        self.toolbar = toolbar(self.canvas)
        self.toolbar.Hide()
        
        #Embed in sizer
        self.Sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.Sizer.Add(self.panel, 0, wx.EXPAND)
        self.Sizer.Add(self.canvas, 0, wx.EXPAND, 8)
        
        
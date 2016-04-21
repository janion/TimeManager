# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 14:56:36 2015

@author: erik_
"""

import wx

import Config

class DataWindow(wx.Dialog):
    
    def __init__(self, parent, idd, logic, index=-1):        
        wx.Dialog.__init__(self, parent, idd, "View data", size=(330, 440),
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
         
        #Open list ctrl to house data
        self.data_list = wx.ListCtrl(self.panel, -1, pos=(10, 60), style=wx.LC_REPORT)

        #Add columns
        self.data_list.InsertColumn(0, "Date", width=80)
        self.data_list.InsertColumn(1, "hours", width=60)
        self.data_list.InsertColumn(2, "Total hours", width=90)
        self.data_list.InsertColumn(3, "Claimed", width=60)
        
        #Bind events
        self.Bind(wx.EVT_CHOICE, self.populateTable, self.proj_choice)
        self.Bind(wx.EVT_SIZE, self.resize)
        
        if index != -1:
            self.proj_choice.SetSelection(index)
            self.populateTable(None)

################################################################################
    
    def resize(self, event):
        event.Skip()
        size = self.GetSize()
        
        self.proj_choice.SetSize((size[0] - 40, -1))
        self.data_list.SetSize((size[0] - 40, size[1] - 110))

################################################################################
    
    def populateTable(self, event): #Extract data from .csv file
        self.data_list.DeleteAllItems()
        
        (days, months, years, hours, cumulative, logged) = self.logic.getProjectData(self.proj_choice.GetStringSelection())
        
        for x in xrange(len(days)):
            self.data_list.InsertStringItem(x, '%02d/%02d/%4d'
                                            %(days[x], months[x], years[x])
                                            )
            self.data_list.SetStringItem(
                x, 1,("%d:%2d" %(int(hours[x]), int(round((hours[x]%1)*60))))
                .replace(" ", "0")
                )
            self.data_list.SetStringItem(
                x, 2, ("%d:%2d" %(int(cumulative[x]), int(round((cumulative[x]%1)*60))))
                .replace(" ", "0")
                )
            self.data_list.SetStringItem(x, 3, str(logged[x]).replace("0", "N").replace("1", "Y"))
        
        self.data_list.SetFocus()

        if Config.hasGraphs:
            
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
            self.MakeDates(days, months, years, hours, cumulative)
            (self.dates, self.wk_hrs) = self.logic.makeDates()
            self.PlotData()
            
            #Bind events
            self.zoom_btn.Bind(wx.EVT_TOGGLEBUTTON, self.Zoom)
            self.pan_btn.Bind(wx.EVT_TOGGLEBUTTON, self.Pan)
            self.home_btn.Bind(wx.EVT_BUTTON, self.Home)

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
        
        
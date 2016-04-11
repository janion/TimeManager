# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 22:48:32 2015

@author: Janion
"""

# Developers' note: csv mode 'rb+' is used rather than 'wb' as 'wb' does not
# have sufficient permissions to write over hidden files
# For creating a file however, 'wb' mode is used as 'rb+' does not have
# sufficient permissions to create a file

"""
time management program

enter projects
click at start of session
or
back date with #hours

charts with amounts done per day


"""

import wx

from dlgs.NewProjectDlg import NewProjectDlg
from dlgs.DataDlg import DataWindow
from dlgs.WorkSessionDlg import WorkSessionDlg
from dlgs.BackdateDlg import BackdateDlg
from processing.ProjectLogic import ProjectLogic as Logic

################################################################################
################################################################################

class Window(wx.Frame):
    def __init__(self, parent, idd, title):
        wx.Frame.__init__(self, parent, idd, title, size=(495, 350))
        self.panel = wx.Panel(self, -1)
        self.SetMinSize(self.GetSize())
        
        self.logic = Logic()
        
        #Create list control to show projects
        self.proj_list = wx.ListCtrl(self.panel, -1, pos=(10, 40),
                                     size=(455, 240), style=wx.LC_REPORT
                                     )

        #Add columns
        self.proj_list.InsertColumn(0, "Project", width=110)
        self.proj_list.InsertColumn(1, "Total hours", width=80)
        self.proj_list.InsertColumn(2, "hours this week", width=95)
        self.proj_list.InsertColumn(3, "Date started", width=75)
        self.proj_list.InsertColumn(4, "Duration (days)", width=95)

        #Get information about each project and add to list ctrl
        for item in self.logic.getProjectNames():
            self.getProjectInfo(item)
            
        self.setupMenu()
        self.createButtons()
        
        self.Bind(wx.EVT_CLOSE, self.onClose)
        self.Bind(wx.EVT_SIZE, self.resize)

################################################################################
    
    def resize(self, event):
        event.Skip()
        size = self.GetSize()
        
        self.proj_list.SetSize((size[0] - 40, size[1] - 110))
#         self.new_btn.SetSize()
#         self.del_btn.SetSize()
#         self.backdate_btn.SetSize()
#         self.start_btn.SetSize()
#         self.data_btn.SetSize()
            
################################################################################

    def createButtons(self):
        #Create buttons
        self.new_btn = wx.Button(self.panel, -1, 'New project', pos=(10, 10))
        self.del_btn = wx.Button(self.panel, -1, 'Close project', pos=(100, 10))
        self.backdate_btn = wx.Button(self.panel, -1, 'Back date', pos=(190, 10))
        self.start_btn = wx.Button(self.panel, -1, 'Start work', pos=(280, 10))
        self.data_btn = wx.Button(self.panel, -1, 'View data', pos=(370, 10))
        
        #Bind events
        self.Bind(wx.EVT_BUTTON, self.newProject, self.new_btn)
        self.Bind(wx.EVT_BUTTON, self.closeProject, self.del_btn)
        self.Bind(wx.EVT_BUTTON, self.backDate, self.backdate_btn)
        self.Bind(wx.EVT_BUTTON, self.startWork, self.start_btn)
        self.Bind(wx.EVT_BUTTON, self.openData, self.data_btn)

################################################################################
            
    def setupMenu(self):
        self.menuBar = wx.MenuBar()
        
        menu1 = wx.Menu()
        menu1.Append(101, "New project")
        menu1.Append(102, "Close Project")
        menu1.AppendSeparator()
        menu1.Append(103, "Quit")
        self.menuBar.Append(menu1, "File")
        
        menu2 = wx.Menu()
        menu2.Append(201, "Backdate")
        menu2.Append(202, "Start work session")
        menu2.AppendSeparator()
        menu2.Append(203, "View data")
        self.menuBar.Append(menu2, "Project")
        
        self.SetMenuBar(self.menuBar)
        
        self.Bind(wx.EVT_MENU, self.newProject, id=101)
        self.Bind(wx.EVT_MENU, self.closeProject, id=102)
        self.Bind(wx.EVT_MENU, self.close, id=103)
        self.Bind(wx.EVT_MENU, self.backDate, id=201)
        self.Bind(wx.EVT_MENU, self.startWork, id=202)
        self.Bind(wx.EVT_MENU, self.openData, id=203)
        
################################################################################
        
    def onClose(self, event):
        self.logic.cleanProjectFiles()
        event.Skip()
        
################################################################################
        
    def close(self, event):
        self.Destroy()
        
################################################################################
        
    def backDate(self, event): #Add time entries without real time recording
        #Open backdating dialog
        dlg = BackdateDlg(self, -1, self.logic)
        dlg.ShowModal()
        
################################################################################
    
    def closeProject(self, event): #Remove a project from the program
        #Open up selection dialog
        dlg = wx.SingleChoiceDialog(self, 'Select a project to be deleted',
                                    'Delete project', self.logic.getProjectNames(),
                                    wx.CHOICEDLG_STYLE
                                    )

        if dlg.ShowModal() == wx.ID_OK:
            #Check user wants to delete project
            name = dlg.GetStringSelection()
            dlg2 = wx.MessageDialog(dlg, 'Are you sure you wish to delete %s?'
                                    %name, 'Delete project?', wx.YES_NO |
                                    wx.NO_DEFAULT
                                    )
            if dlg2.ShowModal() == wx.ID_YES:
                self.logic.deleteProject(name)
                #Remove from listctrl
                self.proj_list.DeleteItem(self.proj_list.FindItem(-1, name))
                #Confirm to user successful deletion
                dlg3 = wx.MessageDialog(dlg2, 'Successfully deleted: %s'
                                        %name, 'Project deleted', wx.OK
                                        )
                dlg3.ShowModal()
                dlg3.Destroy()

        #Close first dialog regardless of deletion or not
        dlg.Destroy()
        
################################################################################
        
    def getProjectInfo(self, item): #Find the relevant data from .csv files
        # Get project information
        projInfo = self.logic.getProjectInfo(item)
        tot = projInfo.getTotalTime()
        this_week = projInfo.getThisWeek()
        proj_start = projInfo.getProjStart()
        tot_days = projInfo.getTotalDays()
         
        #Change total times from decimal hours to time format
        tot_f = "%d:%02d" %(int(tot), int(round((tot % 1) * 60)))
        this_week_f = "%d:%02d" %(int(this_week),
                                 int(round((this_week % 1) * 60))
                                 )
        
        # Update table to show project
        if self.proj_list.FindItem(-1,item) == -1:
            #If project is not currently in the list ctrl then create an entry
            index = self.proj_list.GetItemCount()
            self.proj_list.InsertStringItem(index, item)
            #Then populate that list item
            self.populateList(item, tot_f, this_week_f,
                              proj_start.strftime("%d-%m-%Y"), str(tot_days),
                              index
                              )
        else:
            #Else overwrite current entry
            self.populateList(item, tot_f, this_week_f,
                              proj_start.strftime("%d-%m-%Y"), str(tot_days),
                              self.proj_list.FindItem(-1, item)
                              )
                
################################################################################
        
    def newProject(self, event): #Create new project
        #Open new project dialog
        dlg = NewProjectDlg(self, -1, self.logic)
        dlg.ShowModal()
        dlg.Destroy()
        
################################################################################
        
    def openData(self, event): #Show user data for the selected project
        #Open data dialog
        data_window = DataWindow(self, -1, self.logic, self.proj_list.GetFirstSelected())
        data_window.Show()

################################################################################
            
    def populateList(self, proj, tot, this_week, start, tot_days, index):
        #Add data to given list ctrl entry
        self.proj_list.SetStringItem(index, 1, tot)
        self.proj_list.SetStringItem(index, 2, this_week)
        self.proj_list.SetStringItem(index, 3, start)
        self.proj_list.SetStringItem(index, 4, tot_days)
        
################################################################################
        
    def startWork(self, event): #Allow user to record a work session
        #Open work session dialog
        dlg = WorkSessionDlg(self, -1, self.logic)
        dlg.ShowModal()

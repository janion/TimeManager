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
import csv
import datetime as dt
import os

from dlgs import new
from dlgs import data
from dlgs import worksession
from dlgs import backdate
from Logic import Logic

################################################################################
################################################################################

class Window(wx.Frame):
    def __init__(self, parent, idd, title):
        wx.Frame.__init__(self, parent, idd, title, size=(495, 350))
        self.panel = wx.Panel(self, -1)
        
        self.logic = Logic()
        
        #Create list control to show projects
        self.proj_list = wx.ListCtrl(self.panel, -1, pos=(10, 10),
                                     size=(455, 270), style=wx.LC_REPORT
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
        
    def close(self, event):
        self.Destroy()
        
################################################################################
        
    def backDate(self, event): #Add time entries without real time recording
        #Open backdating dialog
        dlg = backdate.BackDateDlg(self, -1, self.logic)
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
        tot_f = "%d:%2d" %(int(tot), int(round((tot % 1) * 60)))
        tot_f = tot_f.replace(" ", "0")
        this_week_f = "%d:%2d" %(int(this_week),
                                 int(round((this_week % 1) * 60))
                                 )
        this_week_f = this_week_f.replace(" ", "0")
        
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
        dlg = new.NewProjectDlg(self, -1, self.logic)
        dlg.ShowModal()
        dlg.Destroy()
        
################################################################################
        
    def openData(self, event): #Show user data for the selected project
        #Open data dialog
        data_window = data.DataWindow(self, -1, self.logic)
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
        dlg = worksession.WorkSessionDlg(self, -1, self.logic)
        dlg.ShowModal()
        
################################################################################
################################################################################



if __name__ == '__main__':
    app = wx.App()
    fr = Window(None, -1, 'Time manager')
    fr.Show()
    app.MainLoop()
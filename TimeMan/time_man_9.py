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

from dlgs import *#new, data, worksession, backdate

################################################################################
################################################################################

class Window(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(495, 350))
        self.panel = wx.Panel(self, -1)
        
        #Create buttons
        self.new_btn = wx.Button(self.panel, -1, 'New project', pos=(10, 10))
        self.del_btn = wx.Button(self.panel, -1, 'Close project', pos=(100, 10))
        self.backdate_btn = wx.Button(self.panel, -1, 'Back date', pos=(190, 10)
                                      )
        self.start_btn = wx.Button(self.panel, -1, 'Start work', pos=(280, 10))
        self.data_btn = wx.Button(self.panel, -1, 'View data', pos=(370, 10))
        self.data_btn.Enable(False)
        
        #Get project names
        self.GetProjects()
        
        #Create list control to show projects
        self.proj_list = wx.ListCtrl(self.panel, -1, pos=(10, 40),
                                     size=(455, 260), style=wx.LC_REPORT
                                     )
        #Add columns
        self.proj_list.InsertColumn(0, "Project", width=110)
        self.proj_list.InsertColumn(1, "Total hours", width=80)
        self.proj_list.InsertColumn(2, "hours this week", width=95)
        self.proj_list.InsertColumn(3, "Date started", width=75)
        self.proj_list.InsertColumn(4, "Duration (days)", width=95)

        #Get information about each project and add to list ctrl
        for item in self.projects:
            self.GetProjectInfo(item)
        
        #Bind events
        self.Bind(wx.EVT_BUTTON, self.NewProject, self.new_btn)
        self.Bind(wx.EVT_BUTTON, self.DelProject, self.del_btn)
        self.Bind(wx.EVT_BUTTON, self.BackDate, self.backdate_btn)
        self.Bind(wx.EVT_BUTTON, self.StartWork, self.start_btn)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnSelection, self.proj_list)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnDeselection,
                  self.proj_list
                  )
        self.Bind(wx.EVT_BUTTON, self.OpenData, self.data_btn)
        
################################################################################
        
    def BackDate(self, event): #Add time entries without real time recording
        #Open backdating dialog
        dlg = backdate.BackDateDlg(self, -1, 'Back date project', self.projects)
        dlg.ShowModal()
        
################################################################################
    
    def DelProject(self, event): #Remove a project from the program
        #Open up selection dialog
        dlg = wx.SingleChoiceDialog(self, 'Select a project to be deleted',
                                    'Delete project', self.projects,
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
                #Delete file
                os.remove('Project_man_%s.csv' %name)
                #Remove from list of projects
                self.projects.remove(name)
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
        
    def GetProjectInfo(self, item): #Find the relevant data from .csv files
        #Look in the csv file
        with open('Project_man_%s.csv' %item, 'rb') as csvfile:
            r1 = csv.reader(csvfile, delimiter=',')
                
            #Get current date
            now = dt.date.today()
                
            #Iterate over entries to find total hours put into project
            tot = 0. #Total hours
            this_week = 0. #Total hours in last 7 days
            proj_start = None #Empty variable
            for row in r1:
                if proj_start == None: #First line only
                    #Find start date
                    proj_start = dt.date(int(row[2]), int(row[1]), int(row[0]))
                    #Calculate days since project start
                    tot_days = (now - proj_start).days
                try:
                    tot += float(row[3]) #Add hours for each day to total
                        
                    entry = row[0:3] #Get date in list form
                    #Convert to date format
                    entry_date = dt.date(int(entry[2]), int(entry[1]),
                                         int(entry[0])
                                         )
                    if (now - entry_date).days < 7: #Add to week's total
                        this_week += float(row[3])
                except:
                    #If entry doesn't contain valid info, skip it
                    pass
        
        #Change total times from decimal hours to time format
        tot_f = "%d:%2d" %(int(tot), int(round((tot % 1) * 60)))
        tot_f = tot_f.replace(" ", "0")
        this_week_f = "%d:%2d" %(int(this_week),
                                 int(round((this_week % 1) * 60))
                                 )
        this_week_f = this_week_f.replace(" ", "0")
            
        if self.proj_list.FindItem(-1,item) == -1:
            #If project is not currently in the list ctrl then create an entry
            index = self.proj_list.GetItemCount()
            self.proj_list.InsertStringItem(index, item)
            #Then populate that list item
            self.PopulateList(item, tot_f, this_week_f,
                              proj_start.strftime("%d-%m-%Y"), str(tot_days),
                              index
                              )
        else:
            #Else overwrite current entry
            self.PopulateList(item, tot_f, this_week_f,
                              proj_start.strftime("%d-%m-%Y"), str(tot_days),
                              self.proj_list.FindItem(-1, item)
                              )
                              
################################################################################
        
    def GetProjects(self): #Find all projects in home folder
        #Create list
        self.projects = []
        for item in os.listdir(os.getcwd()):
            #Look for project files in directory
            if ('Project_man_' in item and '.csv' in item):
                #Find project name in file name
                self.projects.append(item[12:-4])
                
################################################################################
        
    def NewProject(self, event): #Create new project
        #Open new project dialog
        dlg = new.NewProjectDlg(self, -1, 'New Project')
        dlg.ShowModal()
        dlg.Destroy()

################################################################################
        
    def OnDeselection(self, event): #Disable data from being viewed
        self.data_btn.Enable(False)
        
################################################################################
        
    def OnSelection(self, event): #Enable data to be viewed
        self.data_btn.Enable(True)
        self.current_item = event.m_itemIndex
        
################################################################################
        
    def OpenData(self, event): #Show user data for the selected project
        #Open data dialog
        data_window = data.DataWindow(
            self, -1, self.proj_list.GetItemText(self.current_item)
            )
        data_window.Show()

################################################################################
            
    def PopulateList(self, proj, tot, this_week, start, tot_days, index):
        #Add data to given list ctrl entry
        self.proj_list.SetStringItem(index, 1, tot)
        self.proj_list.SetStringItem(index, 2, this_week)
        self.proj_list.SetStringItem(index, 3, start)
        self.proj_list.SetStringItem(index, 4, tot_days)
        
################################################################################
        
    def StartWork(self, event): #Allow user to record a work session
        #Open work session dialog
        dlg = worksession.WorkSessionDlg(self, -1, 'Work session', self.projects)
        dlg.ShowModal()
        
################################################################################
################################################################################



if __name__ == '__main__':
    app = wx.App()
    fr = Window(None, -1, 'Time manager')
    fr.Show()
    app.MainLoop()
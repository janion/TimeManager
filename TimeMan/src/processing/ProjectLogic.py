'''
Created on 9 Apr 2016

@author: Janion
'''

import os
import datetime as dt
import Constants
from Project import Project
from ProjectInfo import ProjectInfo

class Logic():
    
    class BackdateType():
        UNIQUE = 0
        HAS_ENTRY = 1
        SPILL_OVER = 2
        FUTURE = 3
        
    projects = []

    def __init__(self):
        pass
        
################################################################################
    
    def getProjectFromName(self, name):
        for project in self.projects:
            if project.getName() == name:
                return project
        
        return None
        
################################################################################
    
    def getProjectNames(self): #Find all projects in home folder
        if len(self.projects) == 0:
            self.findProjects()
        
        names = []
        for project in self.projects:
            names.append(project.getName())
        
        return names
        
################################################################################
    
    def findProjects(self): #Find all projects in home folder
        #Create list
        for item in os.listdir(os.getcwd() + "\\" + Constants.fileLocation):
            #Look for project files in directory
            if (item.startswith(Constants.fileStart) and item.endswith(Constants.fileEnd)):
                #Create project object
                self.projects.append(Project(item.strip(Constants.fileStart).strip(Constants.fileEnd)))
        
################################################################################
        
    def deleteProject(self, name):
        #Delete file
        os.remove('%s%s%s%s' %(Constants.fileLocation, Constants.fileStart, name, Constants.fileEnd))
        #Remove from list of projects
        self.projects.remove(self.getProjectFromName(name))
        
################################################################################
        
    def getProjectInfo(self, name):
        project = self.getProjectFromName(name)
        return ProjectInfo(project.getTotalTime(), project.getThisWeek(), project.getProjectStart(), project.getTotalDays())

################################################################################
    
    def getProjectData(self, name):
        project = self.getProjectFromName(name)
        return project.getData()

################################################################################
    
    def makeDates(self, days, months, years, hours, tot): #Make list of dates
    #in range as well as a list of the hours worked on each day.
            
        dates = []
        wk_hrs = []
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
                                dates.append(dt.date(year, month, day))
                                wk_hrs.append(0.0)
                            except:#Skip dates which do not exist
                                pass
                        else: #Add hours worked if date is recorded
                            dates.append(dt.date(year, month, day))
                            wk_hrs.append(hours[count])
                            count += 1
        
        return (dates, wk_hrs)
    
################################################################################

    def getBackdateType(self, name, date, workTime):
        #Find today's date
        today = dt.date.today().strftime("%d-%m-%Y").split('-')
        today = [int(today[0]), int(today[1]), int(today[2])]
             
        #Check date is today or earlier
        if ((date[2] < today[2]) or
            (date[2] == today[2] and date[1] < today[1]) or
            (date[2] == today[2] and date[1] == today[1] and
             date[0] <= today[0])
            ):
            project = self.getProjectFromName(name)
            timeOnDate = project.getWorkOnDate(date)
            
            if timeOnDate == None:
                return self.BackdateType.UNIQUE
            elif timeOnDate + workTime > 24 * 60 * 60:
                return self.BackdateType.SPILL_OVER
            else:
                return self.BackdateType.HAS_ENTRY
        else:
            return self.BackdateType.FUTURE
            
################################################################################

    def insertBackdate(self, name, date, workTime):
        project = self.getProjectFromName(name)
        project.insertBackdate(date, workTime)
            
################################################################################

    def recordSession(self, name, startTime, endTime):
        project = self.getProjectFromName(name)
        project.recordWorkSession(endTime - startTime)
            
################################################################################

    def createNewProjectFile(self, name, date, workTime):
        self.projects.append(Project(name, (date[0], date[1], date[2], workTime)))
            
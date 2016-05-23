'''
Created on 9 Apr 2016

@author: Janion
'''

import os
import shutil
import datetime as dt
import Constants
from Project import Project
from ProjectInfo import ProjectInfo

class ProjectLogic():
    
    class BackdateType():
        UNIQUE = 0
        HAS_ENTRY = 1
        SPILL_OVER = 2
        FUTURE = 3
        
    _projects = []
    _archives = []
    _showArchive = False;

    def __init__(self):
        # Create data folder if it doesn't exist
        if Constants.fileLocation.strip("\\") not in os.listdir(os.getcwd()):
            os.makedirs(Constants.fileLocation)
            
        # Create archive folder if it doesn't exist
        if not os.path.exists(Constants.archiveLocation):
            os.makedirs(Constants.archiveLocation)
            
        self._projects = []
        self._findProjects(Constants.fileLocation, self._projects, False)
        self._archives = []
        self._findProjects(Constants.archiveLocation, self._archives, True)
        
################################################################################
    
    def _getProjectFromName(self, name):
        # Look for project
        for project in self._projects:
            if project.getName() == name:
                return project
        
        # Look for archive
        for project in self._archives:
            if project.getName() == name:
                return project
        
        return None
        
################################################################################
    
    def getProjectNames(self, includeArchive = False): #Find all projects in home folder
        if len(self._projects) == 0:
            self._findProjects(Constants.fileLocation, self._projects, False)
            self._findProjects(Constants.arciveLocation, self._archives, True)
        
        names = []
        for project in self._projects:
            names.append(project.getName())
        if includeArchive:
            for project in self._archives:
                names.append(project.getName())
        
        return names
        
################################################################################
    
    def getArchivedProjectNames(self): #Find all projects in home folder
        if len(self._projects) == 0:
            self._findProjects(Constants.fileLocation, self._projects, False)
            self._findProjects(Constants.arciveLocation, self._archives, True)
        
        names = []
        for project in self._archives:
            names.append(project.getName())
        
        return names
        
################################################################################
    
    def _findProjects(self, directory, ProjectList, isArchive): #Find all projects in home folder
        #Create list
        for item in os.listdir(os.getcwd() + "\\" + directory):
            #Look for project files in directory
            if (item.startswith(Constants.fileStart) and item.endswith(Constants.fileEnd)):
                #Create project object
                ProjectList.append(Project(item.replace(Constants.fileStart, '').replace(Constants.fileEnd, ''), isArchive = isArchive))
        
################################################################################
        
    def deleteProject(self, name):
        #Delete file
        os.remove('%s%s%s%s' %(Constants.fileLocation, Constants.fileStart, name, Constants.fileEnd))
        #Remove from list of projects
        self._projects.remove(self._getProjectFromName(name))
        
################################################################################
        
    def getProjectInfo(self, name):
        project = self._getProjectFromName(name)
        return ProjectInfo(project.getTotalTime(), project.getThisWeek(), project.getProjectStart(), project.getTotalDays())

################################################################################
    
    def getProjectData(self, name):
        project = self._getProjectFromName(name)
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
            timeOnDate = self.getHoursOnDate(name, date)
            
            if timeOnDate == None:
                return self.BackdateType.UNIQUE
            elif timeOnDate + workTime > 24:
                return self.BackdateType.SPILL_OVER
            else:
                return self.BackdateType.HAS_ENTRY
        else:
            return self.BackdateType.FUTURE
            
################################################################################

    def getHoursOnDate(self, name, date):
        project = self._getProjectFromName(name)
        return project.getHoursOnDate(date)
            
################################################################################

    def insertBackdate(self, name, date, workTime):
        project = self._getProjectFromName(name)
        project.insertBackdate(date, workTime)
            
################################################################################

    def recordSession(self, name, workTime):
        project = self._getProjectFromName(name)
        project.recordWorkSession(workTime)
            
################################################################################

    def createNewProjectFile(self, name, date, workTime):
        self._projects.append(Project(name, (date[0], date[1], date[2], workTime)))
            
################################################################################

    def cleanProjectFiles(self):
        for project in self._projects:
            project.clearZeroHourEntries()
            
################################################################################

    def setClaimedHours(self, projectName, claimedIndices):
        project = self._getProjectFromName(projectName)
        project.claimHours(claimedIndices)
            
################################################################################

    def getFormattedData(self, projectName):
        project = self._getProjectFromName(projectName)
        data = project.getData()
        
        fList = []
        states = []
        for x in xrange(len(data[0])):
            hrString = "%2d:%02d" %(int(data[3][x]), int(round((data[3][x] - int(data[3][x])) * 60)))
            fString = "%s - %02d//%02d//%4d" %(hrString, data[0][x], data[1][x], data[2][x])
            fList.append(fString)
            states.append(bool(data[5][x]))
        
        return (fList, states)
            
################################################################################

    def isArchive(self, projectName):
        for project in self._archives:
            if project.getName() == projectName:
                return True
         
        return False
            
################################################################################

    def setShowArchive(self, showArchive):
        self._showArchive = showArchive
            
################################################################################

    def getShowArchive(self):
        return self._showArchive
            
################################################################################

    def archiveProject(self, projectName):
        # Move project file to archive folder
        source = '%s%s%s%s' %(Constants.fileLocation, Constants.fileStart, projectName, Constants.fileEnd)
        destination = '%s%s%s%s' %(Constants.archiveLocation, Constants.fileStart, projectName, Constants.fileEnd)
        if os.path.exists(source):
            shutil.move(source, destination)
            
            # Move project name to archive list
            project = self._getProjectFromName(projectName)
            self._projects.remove(project)
            self._archives.append(project)
            
################################################################################

    def reactivateProject(self, projectName):
        # Move project file to archive folder
        source = '%s%s%s%s' %(Constants.archiveLocation, Constants.fileStart, projectName, Constants.fileEnd)
        destination = '%s%s%s%s' %(Constants.fileLocation, Constants.fileStart, projectName, Constants.fileEnd)
        if os.path.exists(source):
            shutil.move(source, destination)
            
            # Move project name to archive list
            project = self._getProjectFromName(projectName)
            self._archives.remove(project)
            self._projects.append(project)
            
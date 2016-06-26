'''
Created on 24 May 2016

@author: Janion
'''

import os
import datetime as dt
from src.processing import Constants
from src.processing import Project
from src.processing import ProjectInfo

class ProjectBank():
    
    class BackdateType():
        UNIQUE = 0
        HAS_ENTRY = 1
        SPILL_OVER = 2
        FUTURE = 3
        
################################################################################

    def __init__(self):
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
            self._findProjects(Constants.archiveLocation, self._archives, True)
        
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
            self._findProjects(Constants.archiveLocation, self._archives, True)
        
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
        
    def getProjectInfo(self, name):
        project = self._getProjectFromName(name)
        return ProjectInfo(project.getTotalTime(), project.getThisWeek(), project.getProjectStart(), project.getTotalDays())

################################################################################
    
    def getProjectData(self, name):
        project = self._getProjectFromName(name)
        return project.getData()
    
################################################################################

    def getBackdateType(self, name, date, workTime):
        #Find today's date
        today = dt.date.today().strftime("%d-%m-%Y").split('-')
        today = [int(today[0]), int(today[1]), int(today[2])]
             
        #Check date is today or earlier
        if self.isDateValid(date):
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

    def isUniqueProjectName(self, name):
        return name not in self.getProjectNames(True)
            
################################################################################

    def getHoursOnDate(self, name, date):
        project = self._getProjectFromName(name)
        return project.getHoursOnDate(date)
                
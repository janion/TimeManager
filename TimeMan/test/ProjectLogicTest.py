'''
Created on 9 Apr 2016

@author: Janion
'''
import sys
sys.path.insert(0, 'C:\\Users\\Janion\\git\\TimeMan\\TimeMan\\src')

import unittest
import os
import shutil
import datetime as dt
from processing import Constants
from processing.ProjectLogic import ProjectLogic

class Test(unittest.TestCase):

    testDataFiles = ["test0", "test1", "test2"]
    testFileInfo = [[0.05, 0], [1.03, 0], [51.490, 0]]
    newFile = "test3"
#     testCounter = 0
    
#     def setUpConstants(self):
#         self.origLocation = Constants.fileLocation
#         Constants.fileLocation = 'testFolder%d\\' %testCounter
#         testCounter += 1
#         os.mkdir(Constants.fileLocation)
#             
################################################################################
#     
#     def tearDownConstants(self):
#         Constants.fileLocation = self.origLocation
            
################################################################################

    def testShouldFindFiles(self):
        projectLogic = ProjectLogic()
        names = projectLogic.getProjectNames()
        
        self.assertEquals(self.testDataFiles, names)
            
################################################################################

    def testShouldFindProjectFromName(self):
        projectLogic = ProjectLogic()
        for name in projectLogic.getProjectNames():
            project = projectLogic.getProjectFromName(name)
            self.assertIsNotNone(project)
            
        project = projectLogic.getProjectFromName('InvalidProjectName')
        self.assertIsNone(project)
            
################################################################################

    def testShouldFindProjectInfo(self):
        projectLogic = ProjectLogic()
        
        for x in xrange(len(self.testDataFiles)):
            info = projectLogic.getProjectInfo(self.testDataFiles[x])
            self.assertEquals(self.testFileInfo[x][0], round(info.getTotalTime(), 3))
            self.assertEquals(self.testFileInfo[x][1], info.getThisWeek())
            
################################################################################

    def testShouldgetDataFromFile(self):
        projectLogic = ProjectLogic()
        xDays = [20, 24]
        xMonths = [7, 7]
        xYears = [2015, 2015]
        xHours = [0.01, 0.04]
        xCumulativeTotal = [0.01, 0.05]
         
        (days, months, years, hours, CumulativeTotal) = projectLogic.getProjectData(self.testDataFiles[0])
        self.assertEquals(xDays, days)
        self.assertEquals(xMonths, months)
        self.assertEquals(xYears, years)
        self.assertEquals(xHours, hours)
        self.assertEquals(xCumulativeTotal, CumulativeTotal)
            
################################################################################
    
    def testShouldIdentifyValidUniqueBackdate(self):
#         self.setUpConstants()
        
        projName = self.testDataFiles[2]
        projectLogic = ProjectLogic()
        origLocation = Constants.fileLocation
        Constants.fileLocation = 'testShouldIdentifyValidUniqueBackdate\\'
        os.mkdir(Constants.fileLocation)
        shutil.copy("%s%s%s%s" %(origLocation, Constants.fileStart, projName, Constants.fileEnd),
                    "%s%s%s%s" %(Constants.fileLocation, Constants.fileStart, projName, Constants.fileEnd)
                    )
         
        #(True, [days, months, years, hours], [maxx, maxx - minn])
        result = projectLogic.getBackdateType(projName, [1, 2, 2015], 1)
        
        self.assertEquals(result, ProjectLogic.BackdateType.UNIQUE)
        
        os.remove("%s%s%s%s" %(Constants.fileLocation, Constants.fileStart, projName, Constants.fileEnd))
        os.removedirs(Constants.fileLocation)
        Constants.fileLocation = origLocation

#         self.tearDownConstants()
            
################################################################################
    
    def testShouldIdentifyValidHasEntryBackdate(self):
#         self.setUpConstants()
        
        projName = self.testDataFiles[2]
        projectLogic = ProjectLogic()
        origLocation = Constants.fileLocation
        Constants.fileLocation = 'testShouldIdentifyValidHasEntryBackdate\\'
        os.mkdir(Constants.fileLocation)
        shutil.copy("%s%s%s%s" %(origLocation, Constants.fileStart, projName, Constants.fileEnd),
                    "%s%s%s%s" %(Constants.fileLocation, Constants.fileStart, projName, Constants.fileEnd)
                    )
         
        #(True, [days, months, years, hours], [maxx, maxx - minn])
        result = projectLogic.getBackdateType(projName, [1, 1, 2013], 1)
        
        self.assertEquals(result, ProjectLogic.BackdateType.HAS_ENTRY)
        
        os.remove("%s%s%s%s" %(Constants.fileLocation, Constants.fileStart, projName, Constants.fileEnd))
        os.removedirs(Constants.fileLocation)
        Constants.fileLocation = origLocation

#         self.tearDownConstants()
            
################################################################################
    
    def testShouldIdentifyInvalidFutureBackdate(self):
#         self.setUpConstants()
        
        projName = self.testDataFiles[2]
        projectLogic = ProjectLogic()
        origLocation = Constants.fileLocation
        Constants.fileLocation = 'testShouldIdentifyInvalidFutureBackdate\\'
        os.mkdir(Constants.fileLocation)
        shutil.copy("%s%s%s%s" %(origLocation, Constants.fileStart, projName, Constants.fileEnd),
                    "%s%s%s%s" %(Constants.fileLocation, Constants.fileStart, projName, Constants.fileEnd)
                    )
         
        #(True, [days, months, years, hours], [maxx, maxx - minn])
        result = projectLogic.getBackdateType(projName, [1, 2, 3015], 1)
        
        self.assertEquals(result, ProjectLogic.BackdateType.FUTURE)
        
        os.remove("%s%s%s%s" %(Constants.fileLocation, Constants.fileStart, projName, Constants.fileEnd))
        os.removedirs(Constants.fileLocation)
        Constants.fileLocation = origLocation
        
#         self.tearDownConstants()
            
################################################################################
    
    def testShouldIdentifyInvalidSpillOverBackdate(self):
#         self.setUpConstants()
        
        projName = self.testDataFiles[2]
        projectLogic = ProjectLogic()
        origLocation = Constants.fileLocation
        Constants.fileLocation = 'testShouldIdentifyInvalidSpillOverBackdate\\'
        os.mkdir(Constants.fileLocation)
        shutil.copy("%s%s%s%s" %(origLocation, Constants.fileStart, projName, Constants.fileEnd),
                    "%s%s%s%s" %(Constants.fileLocation, Constants.fileStart, projName, Constants.fileEnd)
                    )
         
        #(True, [days, months, years, hours], [maxx, maxx - minn])
        result = projectLogic.getBackdateType(projName, [1, 1, 2013], 23.99)
        
        self.assertEquals(result, ProjectLogic.BackdateType.SPILL_OVER)
        
        os.remove("%s%s%s%s" %(Constants.fileLocation, Constants.fileStart, projName, Constants.fileEnd))
        os.removedirs(Constants.fileLocation)
        Constants.fileLocation = origLocation
        
#         self.tearDownConstants()
            
################################################################################
    
    def testShouldCreateProjectFile(self):
#         self.setUpConstants()
        
        projectLogic = ProjectLogic()
        origLocation = Constants.fileLocation
        Constants.fileLocation = 'testShouldCreateProjectFile\\'
        os.mkdir(Constants.fileLocation)
        
        projectLogic.findProjects()

        for x in xrange(len(self.testDataFiles)):
            projectLogic.createNewProjectFile(self.testDataFiles[x], [1, 1, 2001], 5.55)
            self.assertEquals(self.testDataFiles[0:x+1], projectLogic.getProjectNames())
        
            (days, mnths, yrs, hrs, cumulative) = projectLogic.getProjectData(self.testDataFiles[x])
            self.assertEquals(days, [1])
            self.assertEquals(mnths, [1])
            self.assertEquals(yrs, [2001])
            self.assertEquals(hrs, [5.55])
            self.assertEquals(cumulative, [5.55])
        
        for item in os.listdir(Constants.fileLocation):
            os.remove('%s%s' %(Constants.fileLocation, item))
        os.removedirs(Constants.fileLocation)
        Constants.fileLocation = origLocation
        
#         self.tearDownConstants()

if __name__ == "__main__":
    unittest.main()
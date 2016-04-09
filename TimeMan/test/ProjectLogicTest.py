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
from processing.ProjectLogic import ProjectLogic

class Test(unittest.TestCase):

    testDataFiles = ["test0", "test1", "test2"]
    testFileInfo = [[0.05, 0], [1.03, 0], [51.490, 0]]
    newFile = "test3"

    def testShouldFindFiles(self):
        projectLogic = ProjectLogic()
        names = projectLogic.getProjectNames()
        
        self.assertEquals(self.testDataFiles, names)

    def testShouldFindProjectInfo(self):
        projectLogic = ProjectLogic()
        
        for x in xrange(len(self.testDataFiles)):
            info = projectLogic.getProjectInfo(self.testDataFiles[x])
            self.assertEquals(self.testFileInfo[x][0], round(info.getTotalTime(), 3))
            self.assertEquals(self.testFileInfo[x][1], info.getThisWeek())

    def testShouldgetDataFromFile(self):
        projectLogic = ProjectLogic()
        xDays = [20, 24]
        xMonths = [7, 7]
        xYears = [2015, 2015]
        xHours = [0.01, 0.04]
        xCumulativeTotal = [0.01, 0.05]
         
        (days, months, years, hours, CumulativeTotal) = projectLogic.getData(self.testDataFiles[0])
        self.assertEquals(xDays, days)
        self.assertEquals(xMonths, months)
        self.assertEquals(xYears, years)
        self.assertEquals(xHours, hours)
        self.assertEquals(xCumulativeTotal, CumulativeTotal)
    
    def testShouldIdentifyValidBackdate(self):
        projectLogic = ProjectLogic()
        projectLogic.fileLocation = 'testShouldIdentifyValidBackdate\\'
        os.mkdir(projectLogic.fileLocation)
        shutil.copy("data\\%s%s%s" %(projectLogic.fileStart, self.testDataFiles[2], projectLogic.fileEnd),
                    "%s%s%s%s" %(projectLogic.fileLocation, projectLogic.fileStart, self.testDataFiles[2], projectLogic.fileEnd)
                    )
         
        #(True, [days, months, years, hours], [maxx, maxx - minn])
        result = projectLogic.backdate([1, 2, 2015], self.testDataFiles[2])
        
        self.assertTrue(result[0])
        
        os.remove("%s%s%s%s" %(projectLogic.fileLocation, projectLogic.fileStart, self.testDataFiles[2], projectLogic.fileEnd))
        os.removedirs(projectLogic.fileLocation)
    
    def testShouldIdentifyInvalidBackdate(self):
        projectLogic = ProjectLogic()
        projectLogic.fileLocation = 'testShouldIdentifyInvalidBackdate\\'
        os.mkdir(projectLogic.fileLocation)
        shutil.copy("data\\%s%s%s" %(projectLogic.fileStart, self.testDataFiles[2], projectLogic.fileEnd),
                    "%s%s%s%s" %(projectLogic.fileLocation, projectLogic.fileStart, self.testDataFiles[2], projectLogic.fileEnd)
                    )
         
        #(True, [days, months, years, hours], [maxx, maxx - minn])
        result = projectLogic.backdate([1, 2, 3015], self.testDataFiles[2])
        
        self.assertFalse(result[0])
        
        os.remove("%s%s%s%s" %(projectLogic.fileLocation, projectLogic.fileStart, self.testDataFiles[2], projectLogic.fileEnd))
        os.removedirs(projectLogic.fileLocation)
    
    def testShouldCreateBackdateDataBeforeStartDate(self):
        pass
    
    def testShouldCreateBackdateDataAfterLastDate(self):
        pass
    
    def testShouldCreateBackdateDataBetweenDates(self):
        pass
    
    def testShouldCreateBackdateDataOnPreviouslyUsedDate(self):
        pass
    
    def testShouldCreateBackdateDataToday(self):
        pass
    
    def testShouldRecordSession(self):
        projectLogic = ProjectLogic()
        projectLogic.fileLocation = 'testShouldRecordSession\\'
        os.mkdir(projectLogic.fileLocation)
        
        projectLogic.findProjects()
         
        projectLogic.createNewProjectFile(self.testDataFiles[0], [1, 1, 2001], 5.55)
        projectLogic.recordSession(150, 1950, self.testDataFiles[0])
        
        today = dt.date.today().strftime("%d-%m-%Y").split('-')
        today = [int(today[0]), int(today[1]), int(today[2])]
    
        (days, mnths, yrs, hrs, tot) = projectLogic.getData(self.testDataFiles[0])
        self.assertEquals(days, [1, today[0]])
        self.assertEquals(mnths, [1, today[1]])
        self.assertEquals(yrs, [2001, today[2]])
        self.assertEquals(hrs, [5.55, 0.5])
        self.assertEquals(tot, [5.55, 6.05])
        
        os.remove('%s%s%s%s' %(projectLogic.fileLocation, projectLogic.fileStart, self.testDataFiles[0], projectLogic.fileEnd))
        os.removedirs(projectLogic.fileLocation)
    
    def testShouldCreateProjectFile(self):
        projectLogic = ProjectLogic()
        projectLogic.fileLocation = 'testShouldCreateProjectFile\\'
        os.mkdir(projectLogic.fileLocation)
        
        projectLogic.findProjects()
         
        for x in xrange(len(self.testDataFiles)):
            projectLogic.createNewProjectFile(self.testDataFiles[x], [1, 1, 2001], 5.55)
            self.assertEquals(self.testDataFiles[0:x+1], projectLogic.getProjectNames())
        
            (days, mnths, yrs, hrs, tot) = projectLogic.getData(self.testDataFiles[x])
            self.assertEquals(days, [1])
            self.assertEquals(mnths, [1])
            self.assertEquals(yrs, [2001])
            self.assertEquals(hrs, [5.55])
            self.assertEquals(tot, [5.55])
        
        for item in os.listdir(projectLogic.fileLocation):
            os.remove('%s%s' %(projectLogic.fileLocation, item))
        os.removedirs(projectLogic.fileLocation)

if __name__ == "__main__":
    unittest.main()
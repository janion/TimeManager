'''
Created on 8 Apr 2016

@author: Janion
'''
import sys
sys.path.insert(0, 'C:\\Users\\Janion\\git\\TimeMan\\TimeMan\\src')

import unittest
import os
import shutil
import datetime as dt
from processing.Logic import Logic

class Test(unittest.TestCase):

    testDataFiles = ["test0", "test1", "test2"]
    testFileInfo = [[0.05, 0], [1.03, 0], [51.490, 0]]
    newFile = "test3"

    def testShouldFindFiles(self):
        logic = Logic()
        names = logic.getProjectNames()
        
        self.assertEquals(self.testDataFiles, names)

    def testShouldFindProjectInfo(self):
        logic = Logic()
        
        for x in xrange(len(self.testDataFiles)):
            info = logic.getProjectInfo(self.testDataFiles[x])
            self.assertEquals(self.testFileInfo[x][0], round(info.getTotalTime(), 3))
            self.assertEquals(self.testFileInfo[x][1], info.getThisWeek())

    def testShouldgetDataFromFile(self):
        logic = Logic()
        xDays = [20, 24]
        xMonths = [7, 7]
        xYears = [2015, 2015]
        xHours = [0.01, 0.04]
        xCumulativeTotal = [0.01, 0.05]
         
        (days, months, years, hours, CumulativeTotal) = logic.getData(self.testDataFiles[0])
        self.assertEquals(xDays, days)
        self.assertEquals(xMonths, months)
        self.assertEquals(xYears, years)
        self.assertEquals(xHours, hours)
        self.assertEquals(xCumulativeTotal, CumulativeTotal)
    
    def testShouldIdentifyValidBackdate(self):
        logic = Logic()
        logic.fileLocation = 'testShouldIdentifyValidBackdate\\'
        os.mkdir(logic.fileLocation)
        shutil.copy("data\\%s%s%s" %(logic.fileStart, self.testDataFiles[2], logic.fileEnd),
                    "%s%s%s%s" %(logic.fileLocation, logic.fileStart, self.testDataFiles[2], logic.fileEnd)
                    )
         
        #(True, [days, months, years, hours], [maxx, maxx - minn])
        result = logic.backdate([1, 2, 2015], self.testDataFiles[2])
        
        self.assertTrue(result[0])
        
        os.remove("%s%s%s%s" %(logic.fileLocation, logic.fileStart, self.testDataFiles[2], logic.fileEnd))
        os.removedirs(logic.fileLocation)
    
    def testShouldIdentifyInvalidBackdate(self):
        logic = Logic()
        logic.fileLocation = 'testShouldIdentifyInvalidBackdate\\'
        os.mkdir(logic.fileLocation)
        shutil.copy("data\\%s%s%s" %(logic.fileStart, self.testDataFiles[2], logic.fileEnd),
                    "%s%s%s%s" %(logic.fileLocation, logic.fileStart, self.testDataFiles[2], logic.fileEnd)
                    )
         
        #(True, [days, months, years, hours], [maxx, maxx - minn])
        result = logic.backdate([1, 2, 3015], self.testDataFiles[2])
        
        self.assertFalse(result[0])
        
        os.remove("%s%s%s%s" %(logic.fileLocation, logic.fileStart, self.testDataFiles[2], logic.fileEnd))
        os.removedirs(logic.fileLocation)
    
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
        logic = Logic()
        logic.fileLocation = 'testShouldRecordSession\\'
        os.mkdir(logic.fileLocation)
        
        logic.findProjects()
         
        logic.createNewProjectFile(self.testDataFiles[0], [1, 1, 2001], 5.55)
        logic.recordSession(150, 1950, self.testDataFiles[0])
        
        today = dt.date.today().strftime("%d-%m-%Y").split('-')
        today = [int(today[0]), int(today[1]), int(today[2])]
    
        (days, mnths, yrs, hrs, tot) = logic.getData(self.testDataFiles[0])
        self.assertEquals(days, [1, today[0]])
        self.assertEquals(mnths, [1, today[1]])
        self.assertEquals(yrs, [2001, today[2]])
        self.assertEquals(hrs, [5.55, 0.5])
        self.assertEquals(tot, [5.55, 6.05])
        
        os.remove('%s%s%s%s' %(logic.fileLocation, logic.fileStart, self.testDataFiles[0], logic.fileEnd))
        os.removedirs(logic.fileLocation)
    
    def testShouldCreateProjectFile(self):
        logic = Logic()
        logic.fileLocation = 'testShouldCreateProjectFile\\'
        os.mkdir(logic.fileLocation)
        
        logic.findProjects()
         
        for x in xrange(len(self.testDataFiles)):
            logic.createNewProjectFile(self.testDataFiles[x], [1, 1, 2001], 5.55)
            self.assertEquals(self.testDataFiles[0:x+1], logic.getProjectNames())
        
            (days, mnths, yrs, hrs, tot) = logic.getData(self.testDataFiles[x])
            self.assertEquals(days, [1])
            self.assertEquals(mnths, [1])
            self.assertEquals(yrs, [2001])
            self.assertEquals(hrs, [5.55])
            self.assertEquals(tot, [5.55])
        
        for item in os.listdir(logic.fileLocation):
            os.remove('%s%s' %(logic.fileLocation, item))
        os.removedirs(logic.fileLocation)

if __name__ == "__main__":
    unittest.main()
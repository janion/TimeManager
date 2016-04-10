'''
Created on 10 Apr 2016

@author: Janion
'''
import sys
sys.path.insert(0, 'C:\\Users\\Janion\\git\\TimeMan\\TimeMan\\src')

import unittest
from processing import Constants
from processing.Project import Project

class Test(unittest.TestCase):

    projectNames = ['test0', 'test1', 'test2']

    def testShouldFindCorrectProjectInfo(self):
        pass
            
################################################################################

    def testShouldPopulateDataAndWriteToFile(self):
        project = Project(self.projectNames[0])
        
        xDays = [20, 24]
        xMonths = [7, 7]
        xYears = [2015, 2015]
        xHours = [0.01, 0.04]
        xCumulative = [0.01, 0.05]
        expected = (xDays, xMonths, xYears, xHours, xCumulative)
        
        self.assertEqual(expected, project.getData)
            
################################################################################

    def testShouldReadDataFromFile(self):
        pass
            
################################################################################

    @ExpectError
    def testShouldErrorWhenFileDoesNotExist(self):
        Project('InvalidProjectName')
            
################################################################################
    
    def testShouldCreateBackdateDataBeforeStartDate(self):
        pass
            
################################################################################
    
    def testShouldCreateBackdateDataAfterLastDate(self):
        pass
            
################################################################################
    
    def testShouldCreateBackdateDataBetweenDates(self):
        pass
            
################################################################################
    
    def testShouldCreateBackdateDataOnPreviouslyUsedDate(self):
        pass
            
################################################################################
    
    def testShouldCreateBackdateDataToday(self):
        pass
            
################################################################################
    
    def testShouldRecordSession(self):
        pass
            
################################################################################

    def testShouldNotRecordWorkSessionIfTooShort(self):
        pass
            
################################################################################

    def testShouldWriteDataToFileAndRefreshProjectInfo(self):
        pass
            
################################################################################

    def testShouldWriteDataToFile(self):
        pass
            
################################################################################

    def testShouldGetHoursWorkedOnGivenDate(self):
        pass
            
################################################################################

    def testShouldInsertBackdate(self):
        pass
            
################################################################################
################################################################################


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
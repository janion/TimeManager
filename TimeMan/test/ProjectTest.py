'''
Created on 10 Apr 2016

@author: Janion
'''
import sys
sys.path.insert(0, 'C:\\Users\\Janion\\git\\TimeMan\\TimeMan\\src')

import unittest
import os
import datetime as dt
from processing import Constants
from processing.Project import Project

class Test(unittest.TestCase):

    projectNames = ['test0', 'test1', 'test2']
    newName = 'test3'

    def testShouldFindCorrectProjectInfo(self):
        project = Project(self.projectNames[0])
        
        xStart = dt.date(2015, 7, 20)
        xDuration = (dt.date.today() - xStart).days
        
        self.assertEqual(0.05, project.getTotalTime())
        self.assertEqual(xDuration, project.getTotalDays())
        self.assertEqual(0, project.getThisWeek())
        self.assertEqual(xStart, project.getProjectStart())
            
################################################################################

    def testShouldPopulateDataAndWriteToFile(self):
        data = (1, 1, 2015, 1.02)
        project = Project(self.newName, data)
        expected = ([1], [1], [2015], [1.02], [1.02])
        
        projectName = '%s%s%s' %(Constants.fileStart, self.newName, Constants.fileEnd)
        self.assertTrue(projectName in os.listdir(Constants.fileLocation))
        self.assertEqual(expected, project.getData())
        
        os.remove('%s%s%s%s' %(Constants.fileLocation, Constants.fileStart, self.newName, Constants.fileEnd))
            
################################################################################

    def testShouldReadDataFromFile(self):
        project = Project(self.projectNames[0])
        
        xDays = [20, 24]
        xMonths = [7, 7]
        xYears = [2015, 2015]
        xHours = [0.01, 0.04]
        xCumulative = [0.01, 0.05]
        expected = (xDays, xMonths, xYears, xHours, xCumulative)
        
        self.assertEqual(expected, project.getData())
            
################################################################################

    def testShouldErrorWhenFileDoesNotExist(self):
        try:
            Project('InvalidProjectName')
            self.fail()
        except:
            self.assertTrue(True)
            
################################################################################
    
    def testShouldRecordSession(self):
        today = dt.date.today().strftime("%d-%m-%Y").split('-')
        today = [int(today[0]), int(today[1]), int(today[2])]
        data = (1, 1, 2015, 1.02)
        
        project = Project(self.newName, data)
        workTime = 2.73
        project.recordWorkSession(workTime)
        expected = ([data[0], today[0]],
                    [data[1], today[1]],
                    [data[2], today[2]],
                    [data[3], workTime],
                    [data[3], data[3] + workTime]
                    )
        
        self.assertEqual(expected, project.getData())
        
        os.remove('%s%s%s%s' %(Constants.fileLocation, Constants.fileStart, self.newName, Constants.fileEnd))
            
################################################################################

    def testShouldNotRecordWorkSessionIfTooShort(self):
        data = (1, 1, 2015, 1.02)
        project = Project(self.newName, data)
        expected = ([1], [1], [2015], [1.02], [1.02])
        
        project.recordWorkSession(0.004)
        self.assertEqual(expected, project.getData())
        
        os.remove('%s%s%s%s' %(Constants.fileLocation, Constants.fileStart, self.newName, Constants.fileEnd))
            
################################################################################

    def testShouldWriteDataAndRefresh(self):
        data = (1, 1, 2015, 1.02)
        project = Project(self.newName, data)
        
        (newDay, newMonth, newYear, newHour) = (2, 2, 2015, 2.34)
        project.days.append(newDay)
        project.months.append(newMonth)
        project.years.append(newYear)
        project.hours.append(newHour)
        
        expected = ([data[0], newDay], [data[1], newMonth], [data[2], newYear], [data[3], newHour], [1.02, 3.36])
        project.writeDataAndRefesh()
        
        self.assertEqual(expected, project.getData())
        
        os.remove('%s%s%s%s' %(Constants.fileLocation, Constants.fileStart, self.newName, Constants.fileEnd))
            
################################################################################

    def testShouldGetHoursWorkedOnGivenDate(self):
        data = (1, 1, 2015, 1.02)
        project = Project(self.newName, data)
        
        self.assertEqual(data[3], project.getHoursOnDate([data[0], data[1], data[2]]))
        
        os.remove('%s%s%s%s' %(Constants.fileLocation, Constants.fileStart, self.newName, Constants.fileEnd))
            
################################################################################

    def testShouldInsertBackdateOnDateWithEntry(self):
        data = (1, 1, 2015, 1.02)
        project = Project(self.newName, data)
        
        newHour = 2.34
        project.insertBackdate([data[0], data[1], data[2]], newHour)
        
        expected = ([data[0]], [data[1]], [data[2]], [data[3] + newHour], [data[3] + newHour])
        
        self.assertEqual(expected, project.getData())
        
        os.remove('%s%s%s%s' %(Constants.fileLocation, Constants.fileStart, self.newName, Constants.fileEnd))
            
################################################################################

    def testShouldInsertBackdateOnDateWithoutEntry(self):
        data = (1, 1, 2015, 1.02)
        project = Project(self.newName, data)
        
        (newDay, newMonth, newYear, newHour) = (2, 2, 2015, 2.34)
        project.insertBackdate([newDay, newMonth, newYear], newHour)
        
        expected = ([data[0], newDay], [data[1], newMonth], [data[2], newYear], [data[3], newHour], [1.02, 3.36])
        
        self.assertEqual(expected, project.getData())
        
        os.remove('%s%s%s%s' %(Constants.fileLocation, Constants.fileStart, self.newName, Constants.fileEnd))
            
################################################################################

    def testShouldInsertBackdateBetweenDatesWithEntries(self):
        data = (1, 1, 2015, 1.02)
        project = Project(self.newName, data)
        
        (newDay1, newMonth1, newYear1, newHour1) = (3, 3, 2015, 1.01)
        (newDay2, newMonth2, newYear2, newHour2) = (2, 2, 2015, 2.34)
        project.insertBackdate([newDay1, newMonth1, newYear1], newHour1)
        project.insertBackdate([newDay2, newMonth2, newYear2], newHour2)
        
        expected = ([data[0], newDay2, newDay1],
                    [data[1], newMonth2, newMonth1],
                    [data[2], newYear2, newYear1],
                    [data[3], newHour2, newHour1],
                    [1.02, 3.36, 4.37]
                    )
        
        self.assertEqual(expected, project.getData())
        
        os.remove('%s%s%s%s' %(Constants.fileLocation, Constants.fileStart, self.newName, Constants.fileEnd))
            
################################################################################

    def testShouldInsertBackdateOnDateBeforeFirst(self):
        data = (1, 1, 2015, 1.02)
        project = Project(self.newName, data)
        
        (newDay, newMonth, newYear, newHour) = (2, 2, 2014, 2.34)
        project.insertBackdate([newDay, newMonth, newYear], newHour)
        
        expected = ([newDay, data[0]], [newMonth, data[1]], [newYear, data[2]], [newHour, data[3]], [2.34, 3.36])
        
        self.assertEqual(expected, project.getData())
        
        os.remove('%s%s%s%s' %(Constants.fileLocation, Constants.fileStart, self.newName, Constants.fileEnd))
            
################################################################################
################################################################################


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
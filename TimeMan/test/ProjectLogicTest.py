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
            
################################################################################

    def testShouldFindFiles(self):
        projectLogic = ProjectLogic()
        names = projectLogic.getProjectNames()
        
        self.assertEquals(self.testDataFiles, names)
            
################################################################################

    def testShouldFindProjectFromName(self):
        projectLogic = ProjectLogic()
        for name in projectLogic.getProjectNames():
            project = projectLogic._getProjectFromName(name)
            self.assertIsNotNone(project)
            
        project = projectLogic._getProjectFromName('InvalidProjectName')
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
        xLogged = [0, 0]
         
        (days, months, years, hours, cumulativeTotal, logged) = projectLogic.getProjectData(self.testDataFiles[0])
        self.assertEquals(xDays, days)
        self.assertEquals(xMonths, months)
        self.assertEquals(xYears, years)
        self.assertEquals(xHours, hours)
        self.assertEquals(xCumulativeTotal, cumulativeTotal)
        self.assertEquals(xLogged, logged)
            
################################################################################
    
    def testShouldIdentifyValidUniqueBackdate(self):
        
        projName = self.testDataFiles[2]
        projectLogic = ProjectLogic()
         
        result = projectLogic.getBackdateType(projName, [1, 2, 2015], 1)
        self.assertEquals(result, ProjectLogic.BackdateType.UNIQUE)
            
################################################################################
    
    def testShouldIdentifyValidHasEntryBackdate(self):
        
        projName = self.testDataFiles[2]
        projectLogic = ProjectLogic()
         
        result = projectLogic.getBackdateType(projName, [1, 1, 2013], 1)
        self.assertEquals(result, ProjectLogic.BackdateType.HAS_ENTRY)
            
################################################################################
    
    def testShouldIdentifyInvalidFutureBackdate(self):
        
        projName = self.testDataFiles[2]
        projectLogic = ProjectLogic()
         
        result = projectLogic.getBackdateType(projName, [1, 2, 3015], 1)
        self.assertEquals(result, ProjectLogic.BackdateType.FUTURE)
            
################################################################################
    
    def testShouldIdentifyInvalidSpillOverBackdate(self):
        
        projName = self.testDataFiles[2]
        projectLogic = ProjectLogic()
         
        result = projectLogic.getBackdateType(projName, [1, 1, 2013], 23.99)
        self.assertEquals(result, ProjectLogic.BackdateType.SPILL_OVER)
            
################################################################################
    
    def testShouldCreateProjectFile(self):
         
        testName = "shouldCreateFile"
        projectLogic = ProjectLogic()
 
        projectLogic.createNewProjectFile(testName, [1, 1, 2001], 5.55)
        self.assertEquals(self.testDataFiles + [testName], projectLogic.getProjectNames())
     
        self.assertTrue(os.path.exists("%s%s%s%s" %(Constants.fileLocation, Constants.fileStart,
                                                    testName, Constants.fileEnd))
                        )
        (days, mnths, yrs, hrs, cumulative, logged) = projectLogic.getProjectData(testName)
        self.assertEquals(days, [1])
        self.assertEquals(mnths, [1])
        self.assertEquals(yrs, [2001])
        self.assertEquals(hrs, [5.55])
        self.assertEquals(cumulative, [5.55])
        self.assertEquals(logged, [0])
         
        os.remove('%s%s%s%s' %(Constants.fileLocation, Constants.fileStart, testName, Constants.fileEnd))
            
################################################################################
    
    def testShouldGetArchivedProjectNames(self):
        projectLogic = ProjectLogic()
        
        self.assertEqual(["test3", "test4"], projectLogic.getArchivedProjectNames())
            
################################################################################
    
    def testShouldIdentifyArchivedProject(self):
        projectLogic = ProjectLogic()
        
        self.assertTrue(projectLogic.isArchive("test3"))
        self.assertFalse(projectLogic.isArchive("test2"))
            
################################################################################
    
    def testShouldArchiveAndRectivateProject(self):
        projectLogic = ProjectLogic()
        project = "test0"
        
        self.assertTrue(os.path.exists(Constants.fileLocation + Constants.fileStart + project + Constants.fileEnd))
        self.assertFalse(os.path.exists(Constants.archiveLocation + Constants.fileStart + project + Constants.fileEnd))
        
        projectLogic.archiveProject(project)
        
        self.assertTrue(os.path.exists(Constants.archiveLocation + Constants.fileStart + project + Constants.fileEnd))
        self.assertFalse(os.path.exists(Constants.fileLocation + Constants.fileStart + project + Constants.fileEnd))
        
        projectLogic.reactivateProject(project)
        
        self.assertTrue(os.path.exists(Constants.fileLocation + Constants.fileStart + project + Constants.fileEnd))
        self.assertFalse(os.path.exists(Constants.archiveLocation + Constants.fileStart + project + Constants.fileEnd))
            
################################################################################
    
    def testShouldIdentifyInvalidProjectName(self):
        projectLogic = ProjectLogic()
        
        self.assertTrue(projectLogic.isValidProjectName("Test"))
        
        self.assertFalse(projectLogic.isValidProjectName("Te*st"))
        self.assertFalse(projectLogic.isValidProjectName("Tes&t"))
        self.assertFalse(projectLogic.isValidProjectName("Test@"))
            
################################################################################
    
    def testShouldIdentifyInUseProjectName(self):
        projectLogic = ProjectLogic()
        self.assertFalse(projectLogic.isUniqueProjectName("test0"))
            
################################################################################
    
    def testShouldIdentifyInUseArchivedProjectName(self):
        projectLogic = ProjectLogic()
        self.assertFalse(projectLogic.isUniqueProjectName("test4"))
            
################################################################################
    
    def testShouldIdentifyAvailableProjectName(self):
        projectLogic = ProjectLogic()
        self.assertTrue(projectLogic.isUniqueProjectName("test400"))
            
################################################################################
    
    def testShouldCloseProjectAndDeleteFile(self):
        projectLogic = ProjectLogic()
        testName = "shouldDeleteFile"
        projectLogic.createNewProjectFile(testName, [1, 1, 2001], 1.01)
        self.assertTrue(os.path.exists("%s%s%s%s" %(Constants.fileLocation, Constants.fileStart,
                                                    testName, Constants.fileEnd))
                            )
        
        projectLogic.deleteProject(testName)
        self.assertFalse(os.path.exists("%s%s%s%s" %(Constants.fileLocation, Constants.fileStart,
                                                    testName, Constants.fileEnd))
                            )
            
################################################################################
    
    def testShouldCloseArchivedProject(self):
        projectLogic = ProjectLogic()
        testName = "shouldCloseArchive"
        projectLogic.createNewProjectFile(testName, [1, 1, 2001], 1.01)
        self.assertTrue(os.path.exists("%s%s%s%s" %(Constants.fileLocation, Constants.fileStart,
                                                    testName, Constants.fileEnd))
                            )
        
        projectLogic.archiveProject(testName)
        self.assertTrue(os.path.exists("%s%s%s%s" %(Constants.archiveLocation, Constants.fileStart,
                                                    testName, Constants.fileEnd))
                            )
        
        projectLogic.deleteProject(testName)
        self.assertFalse(os.path.exists("%s%s%s%s" %(Constants.archiveLocation, Constants.fileStart,
                                                    testName, Constants.fileEnd))
                            )
            
################################################################################

if __name__ == "__main__":
    unittest.main()
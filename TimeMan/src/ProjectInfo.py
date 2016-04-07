'''
Created on 7 Apr 2016

@author: Janion
'''

class ProjectInfo():

    def __init__(self, totalTime, thisWeek, projStart, totalDays):
        self.totalTime = totalTime
        self.thisWeek = thisWeek
        self.projStart = projStart
        self.totalDays = totalDays
        
################################################################################
    
    def getTotalTime(self):
        return self.totalTime
        
################################################################################
    
    def getThisWeek(self):
        return self.thisWeek
        
################################################################################
    
    def getProjStart(self):
        return self.projStart
        
################################################################################
    
    def getTotalDays(self):
        return self.totalDays
        
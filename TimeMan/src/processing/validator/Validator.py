'''
Created on 24 May 2016

@author: Janion
'''

import datetime as dt
from src.processing import Constants

class Validator():

    def __init__(self):
        pass
            
################################################################################

    def isDateValid(self, date):
            #Get today's date
            today = dt.date.today().strftime("%d-%m-%Y").split('-')
            today = [int(today[0]), int(today[1]), int(today[2])]
                
            #Check date is today or earlier
            if ((date[2] < today[2]) or
                (date[2] == today[2] and date[1] < today[1]) or
                (date[2] == today[2] and date[1] == today[1] and
                 date[0] <= today[0])
                ):
                return True
            else:
                return False
            
################################################################################

    def isValidProjectName(self, name):
        for character in name:
            if character not in Constants.validFilenameChars:
                return False
        
        return True
            
################################################################################

    def getProjectNameLimit(self):
        return Constants.projectNameLimit
            
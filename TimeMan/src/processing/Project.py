'''
Created on 9 Apr 2016

@author: Janion
'''

import csv
import datetime as dt
import Constants

class Project(object):
    
    name = None
    projStart = None
    days = []
    months = []
    years = []
    hours = []
    cumulative = []
    totalHours = 0
    thisWeek = 0
    totalDays = 0

    def __init__(self, name, data = None):
        self.name = name
        
        if data != None: # Only for a newly created file
            (self.days, self.months, self.years, self.hours, self.cumulative) = data
        else:
            (self.days, self.months, self.years, self.hours, self.cumulative) = self.readFile()
            
        self.findProjectInfo()
        
################################################################################
        
    def recordWorkSession(self, workDuration):
        #Find hours worked in decimal
        hours_worked = round(workDuration / 3600., 2)      
        
        if hours_worked > 0.00: #If a non-zero amount of time has been worked
            #Get name of project and today's date
            today = dt.date.today().strftime("%d-%m-%Y").split('-')
            today = [int(today[0]), int(today[1]), int(today[2])]
            
            if [self.days[-1], self.months[-1], self.years[-1]] == today:
                #Update last entry if it has today's date
                self.hours[-1] += hours_worked
            else:
                #Else make a new entry on the end
                self.days.append(today[0])
                self.months.append(today[1])
                self.years.append(today[2])
                self.hours.append(hours_worked)
            
            self.writeDataAndRefesh()
        
################################################################################
        
    def writeDataAndRefesh(self):
            self.writeDataToFile()
            (self.days, self.months, self.years, self.hours, self.cumulative) = self.readFile()
            self.findProjectInfo()
        
################################################################################
        
    def findProjectInfo(self):
        #Get current date
        now = dt.date.today()
        
        #Find start date
        self.projStart = dt.date(self.years[0], self.months[0], self.days[0])
        #Calculate days since project start
        self.totalDays = (now - self.projStart).days
        self.totalHours = sum(self.hours)
        
        for x in xrange(len(self.days)):
            #Convert to date format
            entry_date = dt.date(self.years[x], self.months[x], self.days[x])
            
            if (now - entry_date).days < 7: #Add to week's total
                self.thisWeek += self.hours[x]
        
################################################################################

    def readFile(self): #Find all the entries in a file
        with open('%s%s%s%s' %(Constants.fileLocation, Constants.fileStart, self.name, Constants.fileEnd), 'rb') as csvfile:
            r1 = csv.reader(csvfile, delimiter=',')
            
            #Declare empty lists
            (days, months, years, hours, cumulative) = ([], [], [], [], [])
            #Find the dates and hours worked
            for row in r1:
                try:
                    result = [int(row[0]), int(row[1]), int(row[2]), float(row[3])]
                except:
                    continue #Skip an erroneous entry
                
                hours.append(result[3])
                years.append(result[2])
                months.append(result[1])
                days.append(result[0])
            
                # Populate cumulative hours list
                if len(cumulative) > 0:
                    cumulative.append(cumulative[-1] + result[3])
                else:
                    cumulative.append(result[3])
            
        return (days, months, years, hours, cumulative)
            
################################################################################

    def writeDataToFile(self):
        #Write to csv file
        with open('%s%s%s%s' %(Constants.fileLocation, Constants.fileStart, self.name, Constants.fileEnd), 'wb') as csvfile:
            csvfile.truncate() #Part of the bodge a few lines above
            w1 = csv.writer(csvfile, delimiter=',')
            for x in xrange(len(self.hours)):
                w1.writerow([self.days[x], self.months[x], self.years[x], self.hours[x]])
    
################################################################################

    def getWorkOnDate(self, date):
        for (day, month, year, workTime) in zip(self.days, self.months, self.years, self.hours):
            if [day, month, year] == date:
                return workTime
        
        return None
    
################################################################################

    def insertBackdate(self, date, workTime):
        beenAdded = False
        
        for x in xrange(len(self.days)):
            if [self.days[x], self.months[x], self.years[x]] == date:
                self.hours[x] += workTime
                beenAdded = True
                
            elif (self.days[x] > date[0] and self.months[x] >= date[1] and self.years[x] >= date[2]):
                self.days.insert(x, date[0])
                self.months.insert(x, date[1])
                self.years.insert(x, date[2])
                self.hours.insert(x, workTime)
                beenAdded = True
        
        if not beenAdded:
            self.days.append(date[0])
            self.months.append(date[1])
            self.years.append(date[2])
            self.hours.append(workTime)
        
        self.writeDataAndRefesh()
        
################################################################################
        
    def getName(self):
        return self.name
        
################################################################################
    
    def getDays(self):
        return self.days
        
################################################################################
    
    def getMonths(self):
        return self.months
        
################################################################################
    
    def getYears(self):
        return self.years
        
################################################################################
    
    def getHours(self):
        return self.hours
        
################################################################################
    
    def getTotalTime(self):
        return self.totalHours
        
################################################################################
    
    def getThisWeek(self):
        return self.thisWeek
        
################################################################################
    
    def getProjectStart(self):
        return self.projStart
        
################################################################################
    
    def getTotalDays(self):
        return self.totalDays
        
################################################################################
    
    def getData(self):
        return (self.days, self.months, self.years, self.hours, self.cumulative)
        
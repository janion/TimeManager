'''
Created on 7 Apr 2016

@author: Janion
'''

import os
import csv
import datetime as dt
from ProjectInfo import ProjectInfo

class Logic():
    
    fileLocation = 'data\\'
    fileStart = 'Project_man_'
    fileEnd = '.csv'
    projects = []

    def __init__(self):
        pass
        
################################################################################
    
    def getProjectNames(self): #Find all projects in home folder
        if len(self.projects) == 0:
            self.findProjects()
        
        return self.projects
        
################################################################################
    
    def findProjects(self): #Find all projects in home folder
        #Create list
        for item in os.listdir(os.getcwd() + "\\" + self.fileLocation):
            #Look for project files in directory
            if (item.startswith(self.fileStart) and item.endswith(self.fileEnd)):
                #Find project name in file name
                self.projects.append(item[12:-4])
        
################################################################################
        
    def deleteProject(self, projectName): #Find the relevant data from .csv files
        #Delete file
        os.remove('%s\\%s%s%s' %(self.fileLocation, self.fileStart, projectName, self.fileEnd))
        #Remove from list of projects
        self.projects.remove(projectName)
        
################################################################################
        
    def getProjectInfo(self, item): #Find the relevant data from .csv files
        #Look in the csv file
        with open('%s\\%s%s%s' %(self.fileLocation, self.fileStart, item, self.fileEnd), 'rb') as csvfile:
            r1 = csv.reader(csvfile, delimiter=',')
                
            #Get current date
            now = dt.date.today()
                
            #Iterate over entries to find total hours put into project
            tot = 0. #Total hours
            this_week = 0. #Total hours in last 7 days
            proj_start = None #Empty variable
            for row in r1:
                if proj_start == None: #First line only
                    #Find start date
                    proj_start = dt.date(int(row[2]), int(row[1]), int(row[0]))
                    #Calculate days since project start
                    tot_days = (now - proj_start).days
                try:
                    tot += float(row[3]) #Add hours for each day to total
                        
                    entry = row[0:3] #Get date in list form
                    #Convert to date format
                    entry_date = dt.date(int(entry[2]), int(entry[1]),
                                         int(entry[0])
                                         )
                    if (now - entry_date).days < 7: #Add to week's total
                        this_week += float(row[3])
                except:
                    #If entry doesn't contain valid info, skip it
                    pass
        
        return ProjectInfo(tot, this_week, proj_start, tot_days)

################################################################################
    
    def getData(self, filename): #Extract data from .csv file
        (days, months, years, hours) = self.readFile(filename)
        cumulative = []
        for entry in hours:
            if len(cumulative) > 0:
                cumulative.append(entry + cumulative[-1])
            else:
                cumulative.append(entry)
        
        return (days, months, years, hours, cumulative)

################################################################################
    
    def makeDates(self, days, months, years, hours, tot): #Make list of dates
    #in range as well as a list of the hours worked on each day.
            
        dates = []
        wk_hrs = []
        count = 0

        for year in xrange(min(years), dt.date.today().year + 1):
            #For years in range
            for month in xrange(1, 13): #For month in each year
                for day in xrange(1, 32): #For day in each month
                    
                    #Provided that the dates are within the range of start to end months
                    if not ((year == years[0] and month < months[0]) or
                            (year == years[-1] and month > months[-1])
                            ):
                    
                        if (day,month,year) not in zip(days, months, years):
                            try: #Add date with zero hours if not recorded
                                dates.append(dt.date(year, month, day))
                                wk_hrs.append(0.0)
                            except:#Skip dates which do not exist
                                pass
                        else: #Add hours worked if date is recorded
                            dates.append(dt.date(year, month, day))
                            wk_hrs.append(hours[count])
                            count += 1
        
        return (dates, wk_hrs)
        
################################################################################

    def readFile(self, name): #Find all the entries in a file
        with open('%s\\%s%s%s' %(self.fileLocation, self.fileStart, name, self.fileEnd), 'rb') as csvfile:
            r1 = csv.reader(csvfile, delimiter=',')
            
            #Declare empty lists
            (days, months, years, hours) = ([], [], [], [])
            #Find the dates and hours worked
            for row in r1:
                try:
                    hours.append(float(row[3]))
                    years.append(int(row[2]))
                    months.append(int(row[1]))
                    days.append(int(row[0]))
                except:
                    pass #Skip an erroneous entry
            
        return (days, months, years, hours)
    
################################################################################

    def backdate(self, date, name): #Find all the entries in a file
        #Find today's date
        today = dt.date.today().strftime("%d-%m-%Y").split('-')
        today = [int(today[0]), int(today[1]), int(today[2])]
            
        #Check date is today or earlier
        if ((date[2] < today[2]) or
            (date[2] == today[2] and date[1] < today[1]) or
            (date[2] == today[2] and date[1] == today[1] and
             date[0] <= today[0])
            ):
            #get data from the csv file
            (days, months, years, hours) = self.readFile(name)
            
            #Cehck if the backdate is earlier than all other entries
            if ((date[2] < years[0]) or
                (date[2] == years[0] and date[1] < months[0]) or
                (date[2] == years[0] and date[1] == months[0] and
                 date[0] < days[0])
                ):
                (minn, maxx) = (-1, 0)
            else:
                minn = -1
                maxx = len(years)
                #Find range of year
                for x in xrange(len(years)):
                    if years[x] < date[2]:
                        minn = x
                    if years[x] > date[2]:
                        maxx = x
                        break
                    
                #Find range of months
                for x in xrange(minn + 1, maxx):
                    if months[x] < date[1]:
                        minn = x
                    if months[x] > date[1]:
                        maxx = x
                        break
                    
                #Find range of days
                for x in xrange(minn + 1, maxx):
                    if days[x] < date[0]:
                        minn = x
                    if days[x] > date[0]:
                        maxx = x
                        break
                    
            return (True, [days, months, years, hours], [maxx, maxx - minn])
        
        else:
            return (False, None, None)
            
################################################################################

    def recordSession(self, startTime, endTime, name):
        #Find hours worked in decimal
        hours_worked = round((endTime - startTime) / 3600., 2)      
        
        if hours_worked > 0.00: #If a non-zero amount of time has been worked
            #Get name of project and today's date
            today = dt.date.today().strftime("%d-%m-%Y").split('-')
            today = [int(today[0]), int(today[1]), int(today[2])]
    
            (days, months, years, hours) = self.readFile(name)
            
            if [days[-1], months[-1], years[-1]] == today:
                #Update last entry if it has today's date
                hours[-1] += hours_worked
            else:
                #Else make a new entry on the end
                days.append(today[0])
                months.append(today[1])
                years.append(today[2])
                hours.append(hours_worked)
            
            self.writeDataToFile(name, days, months, years, hours)
            
################################################################################

    def writeDataToFile(self, name, days, months, years, hours, mode='rb+'):
        #Write to csv file
        with open('%s\\%s%s%s' %(self.fileLocation, self.fileStart, name, self.fileEnd), mode) as csvfile:
            csvfile.truncate() #Part of the bodge a few lines above
            w1 = csv.writer(csvfile, delimiter=',')
            for x in xrange(len(hours)):
                w1.writerow([days[x], months[x], years[x], hours[x]])
            
################################################################################

    def createNewProjectFile(self, name, date, workTime):
        self.writeDataToFile(name, [date[0]], [date[1]], [date[2]], [workTime], 'wb')
        self.projects.append(name)
            
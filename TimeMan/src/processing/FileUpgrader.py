'''
Created on 21 Apr 2016

@author: Janion
'''

import csv
import Constants

def upgradeFiles(projectNames):
    for name in projectNames:
        upgrade_21_04_2016("%s%s%s%s" %(Constants.fileLocation, Constants.fileStart, name, Constants.fileEnd))
        
################################################################################
    
def upgrade_21_04_2016(fileName):
    
    with open(fileName, 'rb') as csvfile:
        r1 = csv.reader(csvfile, delimiter=',')
        contents = [ [], [], [], [], [] ]
        firstRow = True
        
        for row in r1:
            if firstRow:
                firstRow = False
                if len(row) == 5:
                    return
            
            contents[0].append(row[0])
            contents[1].append(row[1])
            contents[2].append(row[2])
            contents[3].append(row[3])
            contents[4].append(0)
    
    with open(fileName, 'wb') as csvfile:
        csvfile.truncate()
        w1 = csv.writer(csvfile, delimiter=',')
        
        for x in xrange(len(contents[0])):
            w1.writerow([ contents[0][x], contents[1][x], contents[2][x], contents[3][x], contents[4][x] ])
    
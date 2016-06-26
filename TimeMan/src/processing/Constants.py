'''
Created on 9 Apr 2016

@author: Janion
'''

import string

fileLocation = 'data\\'
archiveLocation = fileLocation + 'archive\\'
fileStart = 'Project_man_'
fileEnd = '.csv'
validFilenameChars = "-_.() %s%s" % (string.ascii_letters, string.digits)
projectNameLimit = 25
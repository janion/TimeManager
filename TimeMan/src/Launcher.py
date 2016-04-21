'''
Created on 8 Apr 2016

@author: Janion
'''

import wx
import os
from TimeMan import Window
from processing import Constants
from processing import FileUpgrader
    
def getFileNames():
    names = []
    for name in os.listdir(Constants.fileLocation):
        if name.startswith(Constants.fileStart) and name.endswith(Constants.fileEnd):
            names.append(name.replace(Constants.fileStart, '').replace(Constants.fileEnd, ''))
    
    return names

if __name__ == '__main__':
        
    FileUpgrader.upgradeFiles(getFileNames())
        
    app = wx.App()
    fr = Window(None, -1, 'Time manager')
    fr.Show()
    app.MainLoop()
        
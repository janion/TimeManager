'''
Created on 8 Apr 2016

@author: Janion
'''

import wx
from TimeMan import Window

if __name__ == '__main__':
    app = wx.App()
    fr = Window(None, -1, 'Time manager')
    fr.Show()
    app.MainLoop()
from distutils.core import setup
import py2exe
import numpy
from dlgs import Config
import os
import shutil

baseName = 'Launcher'
includes = []
data_files = []

if Config.hasGraphs:
    import matplotlib
    includes = ["matplotlib", "matplotlib.backends",
                "matplotlib.backends.backend_wxagg", "numpy",  "matplotlib.ticker",
                "matplotlib.figure"
                ]
    data_files += matplotlib.get_py2exe_datafiles()
    
excludes = ['_gtkagg', '_tkagg', 'bsddb', 'curses', 'email', 'pywin.debugger',
            'pywin.debugger.dbgcon', 'pywin.dialogs', 'tcl',
            'Tkconstants', 'Tkinter'
            ]
packages = []
dll_excludes = ['libgdk-win32-2.0-0.dll', 'libgobject-2.0-0.dll', 'tcl84.dll',
                'tk84.dll', 'w9xpopen.exe'
                ]
 
setup(
    options = {"py2exe": {"compressed": 2, 
                          "optimize": 1,
                          "includes": includes,
                          "excludes": excludes,
                          "packages": packages,
                          "dll_excludes": dll_excludes,
                          "bundle_files": 3,
                          "dist_dir": "dist",
                          "xref": False,
                          "skip_archive": False,
                          "ascii": False,
                          "custom_boot_script": ''
                         }
              },

    # using zipfile to reduce number of files in dist
    zipfile = 'lib\\library.zip',

    data_files = data_files,
    windows=['%s.py' %baseName]
)

exeFormat = 'dist\\%s.exe'
os.rename(exeFormat %baseName, exeFormat %'TimeManager')
os.mkdir('dist\\data')
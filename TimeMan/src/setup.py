"""from distutils.core import setup
import py2exe
 
setup(windows=['time_man_7.py'])"""

from distutils.core import setup
import py2exe
import matplotlib
 
includes = ["matplotlib", "matplotlib.backends",
            "matplotlib.backends.backend_wxagg", "numpy",  "matplotlib.ticker",
            "matplotlib.figure"#, "_wxagg"
            ]
excludes = ['_gtkagg', '_tkagg', 'bsddb', 'curses', 'email', 'pywin.debugger',
            'pywin.debugger.dbgcon', 'pywin.dialogs', 'tcl',
            'Tkconstants', 'Tkinter'
            ]
packages = []
dll_excludes = ['libgdk-win32-2.0-0.dll', 'libgobject-2.0-0.dll', 'tcl84.dll',
                'tk84.dll'
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
                          "custom_boot_script": '',
                         }
              },
    windows=['TimeMan.py']
)
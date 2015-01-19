# -*- coding: utf-8 -*-
"""

Edited by Christian Münker, 2013
"""
from __future__ import print_function, division, unicode_literals 
import sys, os
# import EITHER PyQt4 OR PySide, depending on your system
from PyQt4 import QtGui, QtCore

from PyQt4.QtGui import QSizePolicy
from PyQt4.QtCore import QSize
#from PySide.QtCore import *
#from PySide.QtGui import *

#import matplotlib as plt
#from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
#from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
#from matplotlib.figure import Figure

import numpy as np
import scipy.signal as sig

if __name__ == "__main__": # relative import if this file is run as __main__
    cwd=os.path.dirname(os.path.abspath(__file__))
    sys.path.append(cwd + '/..')

import databroker as db

from plotUtils import MplWidget#, MplCanvas 

DEBUG = True   

"""
QMainWindow is a class that understands GUI elements like a toolbar, statusbar,
central widget, docking areas. QWidget is just a raw widget.
When you want to have a main window for you project, use QMainWindow.

If you want to create a dialog box (modal dialog), use QWidget, or, 
more preferably, QDialog   
"""       
    
class PlotPhi(QtGui.QMainWindow):

    def __init__(self, parent = None, DEBUG = False): # default parent = None -> top Window 
        super(PlotPhi, self).__init__(parent) # initialize QWidget base class
#        QtGui.QMainWindow.__init__(self) # alternative syntax
        
        self.DEBUG = DEBUG
        
        self.lblWrap = QtGui.QLabel("Wrapped Phase")        
        self.btnWrap = QtGui.QCheckBox()
        self.btnWrap.setChecked(True)
        self.hbox = QtGui.QHBoxLayout()
        self.hbox.addStretch(10)
        self.hbox.addWidget(self.lblWrap)
        self.hbox.addWidget(self.btnWrap)
        self.hbox.addStretch(10)

        self.mplwidget = MplWidget()
#        self.mplwidget.setParent(self)
        
        self.mplwidget.vbox.addLayout(self.hbox)
        
        self.mplwidget.setFocus()
        # make this the central widget, taking all available space:
        self.setCentralWidget(self.mplwidget)
        
        self.draw() # calculate and draw |H(f)|
        
#        #=============================================
#        # Signals & Slots
#        #=============================================          
#        self.mplwidget.sldLw.valueChanged.connect(lambda:self.draw())  
        self.btnWrap.clicked.connect(lambda:self.draw())
            
    def draw(self):
        """ 
        Re-calculate |H(f)| and draw the figure
        """
        self.bb = db.gD['coeffs'][0]
        self.aa = db.gD['coeffs'][1]
        if self.DEBUG:
            print("--- plotPhi.draw() ---") 
            print("b,a = ", self.bb, self.aa)
        [W,H] = sig.freqz(self.bb, self.aa, worN = db.gD['N_FFT']) # calculate H(W) for W = 0 ... pi

        F = W / (2 * np.pi)

        # clear the axes and (re)draw the plot
        #
        mpl = self.mplwidget.ax
        mpl.clear()
        if self.btnWrap.isChecked():
            mpl.plot(F, np.angle(H), lw = db.gD['rc']['lw'])          
        else:
            mpl.plot(F, np.unwrap(np.angle(H)), lw = db.gD['rc']['lw'])
#        mpl.axis([0, 0.5, -db.gD['specs']['A_stop1']-10, 
#                  db.gD['specs']['A_pass1']+1] )
        mpl.set_title(r'Phase transfer function')
        mpl.set_xlabel(r'$F\; \rightarrow $')    
        mpl.set_ylabel(r'$\phi(\mathrm{e}^{\mathrm{j} \Omega})|\; \rightarrow $')    
 
        self.mplwidget.redraw()
        
#------------------------------------------------------------------------------  
    
def main():
    app = QtGui.QApplication(sys.argv)
    form = PlotPhi()
    form.show()
    app.exec_()

if __name__ == "__main__":
    main()
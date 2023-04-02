'''
-----------------------------------------
Description:

Autor: AlbertoGZ
Email: albertogzonline@gmail.com
-----------------------------------------
'''

from select import select
from PySide2 import QtCore, QtWidgets, QtGui
from shiboken2 import wrapInstance
# from collections import OrderedDict

import maya.cmds as cmds
# import maya.mel as mel
import maya.OpenMayaUI as omui
import maya.api.OpenMaya as om
# import re
# import os


# GENERAL VARS
version = '0.1.0'
about = 'by Alberto GZ'
winWidth = 900
winHeight = 800
red = '#872323'
green = '#207527'
lightblue = '#7d654b'
lightpurple = '#604b69'
lightgreen = '#5b694b'

global fromObjectSelected
global toObjectSelected


def getMainWindow():
    main_window_ptr = omui.MQtUtil.mainWindow()
    mainWindow = wrapInstance(int(main_window_ptr), QtWidgets.QWidget)
    return mainWindow


class matchMultiObject(QtWidgets.QMainWindow):

    def __init__(self, parent=getMainWindow()):
        super(matchMultiObject, self).__init__(parent, QtCore.Qt.WindowStaysOnTopHint)

    
    #####################################################
    #                  LAYOUT DESIGN                    #
    #####################################################


        # Creates object, Title Name and Adds a QtWidget as our central widget/Main Layout
        self.setObjectName('matchMultiObjectUI')
        self.setWindowTitle('matchMultiObject' + ' ' + 'v' + version + ' - ' + about)
        mainLayout = QtWidgets.QWidget(self)
        self.setCentralWidget(mainLayout)

        
        # Adding a Horizontal layout to divide the UI in columns
        columns = QtWidgets.QHBoxLayout(mainLayout)

        # Creating N vertical layout
        self.col1 = QtWidgets.QVBoxLayout()
        self.col2 = QtWidgets.QVBoxLayout()
        self.col3 = QtWidgets.QVBoxLayout()
        self.col4 = QtWidgets.QVBoxLayout()
        self.col5 = QtWidgets.QVBoxLayout()
        

        # Set columns for each layout using stretch policy
        columns.addLayout(self.col1, 3)
        columns.addLayout(self.col2, 0)
        columns.addLayout(self.col3, 3)
        columns.addLayout(self.col4, 3)
        columns.addLayout(self.col5, 3)
    

        # Adding layouts
        layout1 = QtWidgets.QVBoxLayout()
        layout1 = QtWidgets.QVBoxLayout()
        layout1A = QtWidgets.QVBoxLayout()
        layout1B = QtWidgets.QHBoxLayout()
        layout2 = QtWidgets.QGridLayout(alignment=QtCore.Qt.AlignTop)
        layout3 = QtWidgets.QVBoxLayout()
        layout3A = QtWidgets.QVBoxLayout()
        layout3B = QtWidgets.QHBoxLayout()
        layout4 = QtWidgets.QGridLayout()
        layout5 = QtWidgets.QGridLayout(alignment=QtCore.Qt.AlignTop)
    
        
        self.col1.addLayout(layout1)
        self.col2.addLayout(layout2)
        self.col3.addLayout(layout3)   
        self.col4.addLayout(layout4)      
        self.col5.addLayout(layout5) 
    
        layout1.addLayout(layout1A)
        layout1.addLayout(layout1B)
        layout2.addLayout(layout2, 1, 1)
        layout3.addLayout(layout3A)
        layout3.addLayout(layout3B)
        layout4.addLayout(layout4, 1, 1)
        layout5.addLayout(layout5, 1, 1)
        
       

    #####################################################
    #                     UI ELEMENTS                   #
    #####################################################

        ### "FROM OBJECT" SECTION
        #

        # Caption (fromObject)
        self.fromObjectLabel = QtWidgets.QLabel("FROM ")
        self.fromObjectLabel.setFixedHeight(70)
        self.fromObjectLabel.setStyleSheet("border: 3px solid"+lightgreen+';border-bottom:0; border-top-left-radius:12px; border-top-right-radius:12px')
        self.fromObjectLabel.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)

        # Filter object type (fromObject)
        self.fromObjectFilterLabel = QtWidgets.QLabel('Show:')
        self.fromObjectFilterVisibleChk = QtWidgets.QCheckBox('Visible nodes only')
        self.fromObjectFilterVisibleChk.setChecked(True)
        self.fromObjectFilterVisibleChk.setStyleSheet('background-color:' + lightgreen)
        self.fromObjectFilterVisibleChk.stateChanged.connect(self.fromObjectReload)
        self.fromObjectFilterRefNodesChk = QtWidgets.QCheckBox('Reference nodes only')
        self.fromObjectFilterRefNodesChk.setStyleSheet('background-color:' + lightgreen)
        self.fromObjectFilterRefNodesChk.stateChanged.connect(self.fromObjectReload)
        
       
        # SearchBox input for filter list (fromObject)
        self.fromObjectSearchBox = QtWidgets.QLineEdit('', self)
        self.fromObjectRegex = QtCore.QRegExp('[0-9A-Za-z_]+')
        self.fromObjectValidator = QtGui.QRegExpValidator(self.fromObjectRegex)
        self.fromObjectSearchBox.setValidator(self.fromObjectValidator)
        self.fromObjectSearchBox.textChanged.connect(self.fromObjectFilter)
        self.fromObjectSearchBox.setStyleSheet('background-color:' + lightgreen)
        self.fromObjectSearchBox.setPlaceholderText("Search...")

        # List of objects (fromObject)
        self.fromObjectQList = QtWidgets.QListWidget(self)
        self.fromObjectQList.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.fromObjectQList.setMinimumWidth(150)
        self.fromObjectQList.itemSelectionChanged.connect(self.fromObjectSel)
        self.fromObjectQList.setStyleSheet('background-color:' + lightgreen)

        self.fromObjectSelectLabel = QtWidgets.QLabel('Select')
        
        # All button select (fromObject)
        self.fromObjectSelectAllBtn = QtWidgets.QPushButton('All')
        self.fromObjectSelectAllBtn.setFixedWidth(70)
        self.fromObjectSelectAllBtn.clicked.connect(self.fromObjectSelectAll)
        self.fromObjectSelectAllBtn.setStyleSheet('background-color:' + lightgreen)

        # None button select (fromObject)
        self.fromObjectSelectNoneBtn = QtWidgets.QPushButton('None')
        self.fromObjectSelectNoneBtn.setFixedWidth(70)
        self.fromObjectSelectNoneBtn.clicked.connect(self.fromObjectSelectNone)
        self.fromObjectSelectNoneBtn.setStyleSheet('background-color:' + lightgreen)

        # Reload button (fromObject)
        self.fromObjectReloadBtn = QtWidgets.QPushButton('Reload')
        self.fromObjectReloadBtn.clicked.connect(self.fromObjectReload)
        self.fromObjectReloadBtn.setStyleSheet('background-color:' + lightgreen)



        ### "TO OBJECT" SECTION
        #
        # Caption (toObject)
        self.toObjectLabel = QtWidgets.QLabel("TO ")
        self.toObjectLabel.setFixedHeight(70)
        self.toObjectLabel.setStyleSheet("border: 3px solid"+lightpurple+';border-bottom:0; border-top-left-radius:12px; border-top-right-radius:12px')
        self.toObjectLabel.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)

        # Filter object type (toObject)
        self.toObjectFilterLabel = QtWidgets.QLabel('Show:')
        self.toObjectFilterVisibleChk = QtWidgets.QCheckBox('Visible nodes only')
        self.toObjectFilterVisibleChk.setChecked(True)
        self.toObjectFilterVisibleChk.setStyleSheet('background-color:' + lightpurple)
        self.toObjectFilterVisibleChk.stateChanged.connect(self.toObjectReload)
        self.toObjectFilterRefNodesChk = QtWidgets.QCheckBox('Reference nodes only')
        self.toObjectFilterRefNodesChk.setStyleSheet('background-color:' + lightpurple)
        self.toObjectFilterRefNodesChk.stateChanged.connect(self.toObjectReload)
       
        # SearchBox input for filter list (toObject)
        self.toObjectSearchBox = QtWidgets.QLineEdit('', self)
        self.toObjectRegex = QtCore.QRegExp('[0-9A-Za-z_]+')
        self.toObjectValidator = QtGui.QRegExpValidator(self.toObjectRegex)
        self.toObjectSearchBox.setValidator(self.toObjectValidator)
        self.toObjectSearchBox.textChanged.connect(self.toObjectFilter)
        self.toObjectSearchBox.setStyleSheet('background-color:' + lightpurple)
        self.toObjectSearchBox.setPlaceholderText("Search...")

        # List of objects (toObject)
        self.toObjectQList = QtWidgets.QListWidget(self)
        self.toObjectQList.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.toObjectQList.setMinimumWidth(150)
        self.toObjectQList.itemSelectionChanged.connect(self.toObjectSel)
        self.toObjectQList.setStyleSheet('background-color:' + lightpurple)

        self.selecttoObjectLabel = QtWidgets.QLabel('Select')
        
        # All button select (toObject)
        self.toObjectSelectAllBtn = QtWidgets.QPushButton('All')
        self.toObjectSelectAllBtn.setFixedWidth(70)
        self.toObjectSelectAllBtn.clicked.connect(self.toObjectSelectAll)
        self.toObjectSelectAllBtn.setStyleSheet('background-color:' + lightpurple)

        # None button select (toObject)
        self.toObjectSelectNoneBtn = QtWidgets.QPushButton('None')
        self.toObjectSelectNoneBtn.setFixedWidth(70)
        self.toObjectSelectNoneBtn.clicked.connect(self.toObjectSelectNone)
        self.toObjectSelectNoneBtn.setStyleSheet('background-color:' + lightpurple)

        # Reload button (toObject)
        self.toObjectSelectReloadBtn = QtWidgets.QPushButton('Reload')
        self.toObjectSelectReloadBtn.clicked.connect(self.toObjectReload)
        self.toObjectSelectReloadBtn.setStyleSheet('background-color:' + lightpurple)
    

        
        # Status bar
        self.statusBar = QtWidgets.QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.messageChanged.connect(self.statusChanged)

        # Spacer
        separator = QtWidgets.QWidget()
        separator.setFixedHeight(2)
        separator.setStyleSheet("background-color:rgb(255,0,0)")


        # Match button
        self.matchBtn = QtWidgets.QPushButton('Match')
        self.matchBtn.clicked.connect(self.match)
        #self.matchBtn.setStyleSheet('background-color:' + lightblue)

        # Match transforms checkboxes
        self.matchPositionChk = QtWidgets.QCheckBox('Position')
        self.matchPositionChk.setChecked(True)
        self.matchPositionChk.stateChanged.connect(self.matchBtnStatus)
        self.matchRotationChk = QtWidgets.QCheckBox('Rotation')
        self.matchRotationChk.setChecked(True)
        self.matchRotationChk.stateChanged.connect(self.matchBtnStatus)
        self.matchScaleChk = QtWidgets.QCheckBox('Scale')
        self.matchScaleChk.setChecked(True)
        self.matchScaleChk.stateChanged.connect(self.matchBtnStatus)


        #### Adding all elements to layouts
        layout1A.addWidget(self.fromObjectLabel)
        layout1A.addWidget(self.fromObjectSearchBox)
        layout1A.addWidget(self.fromObjectQList)
        layout1A.addWidget(self.fromObjectFilterVisibleChk)
        layout1A.addWidget(self.fromObjectFilterRefNodesChk)
        layout1B.addWidget(self.fromObjectSelectLabel)
        layout1B.addWidget(self.fromObjectSelectAllBtn)
        layout1B.addWidget(self.fromObjectSelectNoneBtn)
        layout1A.addWidget(self.fromObjectReloadBtn)

        layout3A.addWidget(self.toObjectLabel)
        layout3A.addWidget(self.toObjectSearchBox)
        layout3A.addWidget(self.toObjectQList)
        layout3A.addWidget(self.toObjectFilterVisibleChk)
        layout3A.addWidget(self.toObjectFilterRefNodesChk)
        layout3B.addWidget(self.selecttoObjectLabel)
        layout3B.addWidget(self.toObjectSelectAllBtn)
        layout3B.addWidget(self.toObjectSelectNoneBtn)
        layout3A.addWidget(self.toObjectSelectReloadBtn)

        layout4.addWidget(self.matchPositionChk)
        layout4.addWidget(self.matchRotationChk)
        layout4.addWidget(self.matchScaleChk)
        layout4.addWidget(self.matchBtn)

       
        self.resize(winWidth, winHeight)    


        
        
    #####################################################
    #                 INIT FUNCTIONS                    #
    #####################################################

        self.fromObjectLoad()
        self.fromObjectSelectNone()
        self.toObjectLoad()
        self.toObjectSelectNone()
        




    #####################################################
    #                      FUNCTIONS                    #
    #####################################################

    ### "FROM OBJECT" SECTION
    #
    def fromObjectFilter(self):
        textFilter = str(self.fromObjectSearchBox.text()).lower()
        if not textFilter:
            for row in range(self.fromObjectQList.count()):
                self.fromObjectQList.setRowHidden(row, False)
        else:
            for row in range(self.fromObjectQList.count()):
                if textFilter in str(self.fromObjectQList.item(row).text()).lower():
                    self.fromObjectQList.setRowHidden(row, False)
                else:
                    self.fromObjectQList.setRowHidden(row, True)


    def fromObjectLoad(self):
        fromObjectType = 'transform'
        global fromObjectList

        if self.fromObjectFilterVisibleChk.isChecked() == True:
            fromObjectVisible = 1
        else:
            fromObjectVisible = 0

        if self.fromObjectFilterRefNodesChk.isChecked() == True:
            fromObjectRefs = 1
        else:
            fromObjectRefs = 0

        fromObjectList = []
        fromObjectList.append(cmds.ls(type=fromObjectType, v=fromObjectVisible, dag=1, rn=fromObjectRefs))
        
        for fromObject in fromObjectList:
            # fromObject = [w.replace('Shape', '') for w in fromObject]
            fromObject.sort()
            self.fromObjectQList.addItems(fromObject)


    ### Get selected items in fromObjectQList
    def fromObjectSel(self):
        global fromObjectSelected

        items = self.fromObjectQList.selectedItems()
        fromObjectSelected = []
        for i in items:
            fromObjectSelected.append(i.text())

            if len(fromObjectSelected) < 1:
                self.fromObjectLabel.setText('FROM ')
            else:   
                self.fromObjectLabel.setText('FROM '+str(len(fromObjectSelected)))
        
        return fromObjectSelected
        #self.statusBar.showMessage(str(fromObjectSelected), 4000) #for testing


    def fromObjectSelectAll(self):
        self.fromObjectQList.selectAll()

        
    def fromObjectSelectNone(self):
        fromObjectSelected = []
        self.fromObjectQList.clearSelection()
        if fromObjectSelected != []:
            del fromObjectSelected[:]
        self.fromObjectLabel.setText('FROM ')

    
    def fromObjectReload(self):
        self.fromObjectQList.clear()
        del fromObjectSelected[:]
        self.fromObjectLabel.setText('FROM ')
        self.fromObjectLoad()

    

        


    ### "TO OBJECT" SECTION
    #
    def toObjectFilter(self):
        textFilter = str(self.toObjectSearchBox.text()).lower()
        if not textFilter:
            for row in range(self.toObjectQList.count()):
                self.toObjectQList.setRowHidden(row, False)
        else:
            for row in range(self.toObjectQList.count()):
                if textFilter in str(self.toObjectQList.item(row).text()).lower():
                    self.toObjectQList.setRowHidden(row, False)
                else:
                    self.toObjectQList.setRowHidden(row, True)


    def toObjectLoad(self):
        toObjectType = 'transform'
        global toObjectList

        if self.toObjectFilterVisibleChk.isChecked() == True:
            toObjectVisible = 1
        else:
            toObjectVisible = 0

        if self.toObjectFilterRefNodesChk.isChecked() == True:
            toObjectRefs = 1
        else:
            toObjectRefs = 0

        toObjectList = []
        toObjectList.append(cmds.ls(type=toObjectType, v=toObjectVisible, dag=1, rn=toObjectRefs))

        for toObject in toObjectList:
            #toObject = [w.replace('Shape', '') for w in toObject]
            toObject.sort()
            self.toObjectQList.addItems(toObject)


    ### Get selected items in toObjectQList
    def toObjectSel(self):
        global toObjectSelected

        items = self.toObjectQList.selectedItems()
        toObjectSelected = []
        for i in items:
            toObjectSelected.append(i.text())

            if len(toObjectSelected) < 1:
                self.toObjectLabel.setText('TO ')
            else:   
                self.toObjectLabel.setText('TO '+str(len(toObjectSelected)))
        
        return toObjectSelected
        #self.statusBar.showMessage(str(toObjectSelected), 4000) #for testing

    
    def toObjectSelectAll(self):
        self.toObjectQList.selectAll()

        
    def toObjectSelectNone(self):
        toObjectSelected = []
        self.toObjectQList.clearSelection()
        if toObjectSelected != []:
            del toObjectSelected[:]
        self.toObjectLabel.setText('TO ')


    def toObjectReload(self):
        self.toObjectQList.clear()
        del toObjectSelected[:]
        self.toObjectLoad()
        self.toObjectLabel.setText('TO ')
        

    
    
    ### MATCH
    def match(self):            
        
        for f, t in zip(fromObjectSelected, toObjectSelected):

            if self.matchPositionChk.isChecked() == True:
                posStatus = True
            else:
                posStatus = False

            if self.matchRotationChk.isChecked() == True:
                rotStatus = True
            else:
                rotStatus = False

            if self.matchScaleChk.isChecked() == True:
                sclStatus = True
            else:
                sclStatus = False
            
            
            cmds.matchTransform(f, t, pos=posStatus, rot=rotStatus, scl=sclStatus)
            #self.statusBar.showMessage(str(posStatus)+str(rotStatus)+str(sclStatus), 4000)


    def matchBtnStatus(self):
        if self.matchPositionChk.isChecked() == False and self.matchRotationChk.isChecked() == False and self.matchScaleChk.isChecked() == False:
            self.matchBtn.setEnabled(False)
        elif self.matchPositionChk.isChecked() == True or self.matchRotationChk.isChecked() == True or self.matchScaleChk.isChecked() == True:
            self.matchBtn.setEnabled(True)


    def statusChanged(self, args):
        if not args:
            self.statusBar.setStyleSheet('background-color:none')
      

     
    def closeEvent(self, event):
        del fromObjectSelected[:]
        del toObjectSelected[:]
        pass






#####################################################
#                    INIT WINDOW                    #
#####################################################

if __name__ == '__main__':
    win = matchMultiObject(parent=getMainWindow())
    try:
        win.close()
    except:
        pass
  
    win.show()
    win.raise_()

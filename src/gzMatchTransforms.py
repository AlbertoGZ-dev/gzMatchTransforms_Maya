'''
████████████████████████████████████████████████████████████████████████████
    
    gzMatchTransforms for Maya
    
    Description: gzMatchTransforms makes match transformations on 
    multiple objects by paired objects given a first selection list 
    for the origin objects and second selection list to target objects. 
    
    Author: AlbertoGZ
    albertogzonline@gmail.com
    https://github.com/AlbertoGZ-dev

████████████████████████████████████████████████████████████████████████████

'''

from PySide2 import QtCore, QtWidgets, QtGui
from shiboken2 import wrapInstance
from pathlib import Path

import maya.cmds as cmds
import maya.OpenMayaUI as omui
import maya.api.OpenMaya as om
import json
import os


# GENERAL VARS
title = 'gzMatchTransforms'
version = '0.1.2'
about = 'by AlbertoGZ'
winWidth = 500
winHeight = 600
scriptPath = os.path.dirname(__file__)
configFile = ''
gzMatchTransformsLogo = scriptPath+'/icons/gzMatchTransformsIcon.png'
icon = QtGui.QIcon(gzMatchTransformsLogo)
pixmap = QtGui.QPixmap(gzMatchTransformsLogo)

# colors
red = '#872323'
green = '#207527'
lightbrown = '#7d654b'
lightpurple = '#604b69'
lightgreen = '#5b694b'
lightblue = '#3e5158'
lightgrey = '#999'
midgrey = '#777'
darkgrey = '#111'
darkgrey2 = '#222'
magent = '#b31248'
cyan = '#07888c'
yellow = '#c7b600'
orange = '#b8810a'
white = '#c9c9c9'
black = '#1a1a1a'


fromObjectSelected = []
toObjectSelected = []


def getMainWindow():
    main_window_ptr = omui.MQtUtil.mainWindow()
    mainWindow = wrapInstance(int(main_window_ptr), QtWidgets.QWidget)
    return mainWindow

class gzMatchTransforms(QtWidgets.QMainWindow):

    def __init__(self, parent=getMainWindow()):
        super(gzMatchTransforms, self).__init__(parent, QtCore.Qt.WindowStaysOnTopHint)

    

        #####################################################
        #               MAIN LAYOUT DESIGN                  #
        #####################################################

        # Creates object, Title Name and Adds a QtWidget as our central widget/Main Layout
        self.setObjectName('gzMatchTransformsUI')
        self.setWindowTitle(title + ' ' + 'v' + version + ' - ' + about)
        self.setWindowIcon(icon)

        self.tabs = QtWidgets.QTabWidget(self)
        self.tabs.setStyleSheet('background-color:' + darkgrey2)

        tab1Layout = QtWidgets.QWidget(self)
        tab2Layout = QtWidgets.QWidget(self)

        self.tabs.addTab(tab1Layout, 'Match')
        self.tabs.addTab(tab2Layout, 'About')

        self.tabs.currentChanged.connect(self.onTabChange)
       
        self.tabs.setStyleSheet('QTabWidget::pane {border: 1px solid' + magent + ';}' 'QTabBar::tab:selected {background-color:'+ magent +';}')

        self.setCentralWidget(self.tabs)



        '''
        |‾‾‾‾‾‾\________________________________________
        |                                               |
        |   MATCH TAB                                   |
        |                                               |
                                                      '''
        ### LAYOUT
        # Creating layouts
        rows = QtWidgets.QVBoxLayout(tab1Layout)
        
        # Creating N horizontal layout
        row1 = QtWidgets.QHBoxLayout()
        row2 = QtWidgets.QVBoxLayout()

        # Creating N vertical layout
        col1 = QtWidgets.QVBoxLayout()
        col2 = QtWidgets.QVBoxLayout()

        layout1 = QtWidgets.QVBoxLayout()
        layout1A = QtWidgets.QVBoxLayout()
        layout1B = QtWidgets.QHBoxLayout()
        
        layout2 = QtWidgets.QVBoxLayout()
        layout2A = QtWidgets.QVBoxLayout()
        layout2B = QtWidgets.QHBoxLayout()
       
        layout3 = QtWidgets.QHBoxLayout(alignment=QtCore.Qt.AlignCenter | QtCore.Qt.AlignBottom)
        layout4 = QtWidgets.QHBoxLayout()
       
        # Adding layouts
        rows.addLayout(row1, 0)
        rows.addLayout(row2, 1)
        
        row1.addLayout(col1, 1)
        row1.addLayout(col2, 1)
        
        col1.addLayout(layout1)
        col2.addLayout(layout2)
        row2.addLayout(layout3)
        row2.addLayout(layout4)
      
        layout1.addLayout(layout1A)
        layout1.addLayout(layout1B)
        layout2.addLayout(layout2A)
        layout2.addLayout(layout2B)

     
       
        #####################################################
        #                     UI ELEMENTS                   #
        #####################################################

        ### "FROM OBJECT" SECTION
        #

        # Caption (fromObject)
        self.fromObjectLabel = QtWidgets.QLabel("FROM ")
        self.fromObjectLabel.setFixedHeight(70)
        self.fromObjectLabel.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        #self.fromObjectLabel.setStyleSheet('background-color:' + black)

        # Get selected button (fromObject)
        self.fromObjectGetSelectedBtn = QtWidgets.QPushButton('Get selected')
        self.fromObjectGetSelectedBtn.setStyleSheet('background-color:' + black)
        self.fromObjectGetSelectedBtn.clicked.connect(self.fromObjectGetSelected)

        # Filter object type (fromObject)
        self.fromObjectFilterLabel = QtWidgets.QLabel('Show:')
        self.fromObjectFilterVisibleChk = QtWidgets.QCheckBox('Visible nodes only')
        self.fromObjectFilterVisibleChk.setChecked(True)
        self.fromObjectFilterVisibleChk.setStyleSheet('background-color:' + black)
        self.fromObjectFilterVisibleChk.stateChanged.connect(self.fromObjectReload)
        self.fromObjectFilterRefNodesChk = QtWidgets.QCheckBox('Reference nodes only')
        self.fromObjectFilterRefNodesChk.setStyleSheet('background-color:' + black)
        self.fromObjectFilterRefNodesChk.stateChanged.connect(self.fromObjectReload)
        self.fromObjectFilterTopNodesChk = QtWidgets.QCheckBox('Top nodes only')
        self.fromObjectFilterTopNodesChk.setStyleSheet('background-color:' + black)
        self.fromObjectFilterTopNodesChk.stateChanged.connect(self.fromObjectReload)
        
        # SearchBox input for filter list (fromObject)
        self.fromObjectSearchBox = QtWidgets.QLineEdit('', self)
        self.fromObjectRegex = QtCore.QRegExp('[0-9A-Za-z_]+')
        self.fromObjectValidator = QtGui.QRegExpValidator(self.fromObjectRegex)
        self.fromObjectSearchBox.setValidator(self.fromObjectValidator)
        self.fromObjectSearchBox.textChanged.connect(self.fromObjectFilter)
        self.fromObjectSearchBox.setStyleSheet('background-color:' + black)
        self.fromObjectSearchBox.setPlaceholderText("Search...")

        # List of objects (fromObject)
        self.fromObjectQList = QtWidgets.QListWidget(self)
        self.fromObjectQList.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.fromObjectQList.setMinimumWidth(150)
        self.fromObjectQList.itemSelectionChanged.connect(self.fromObjectSel)
        self.fromObjectQList.setStyleSheet('background-color:' + black)

        self.fromObjectSelectLabel = QtWidgets.QLabel('Select')
        
        # All button select (fromObject)
        self.fromObjectSelectAllBtn = QtWidgets.QPushButton('All')
        self.fromObjectSelectAllBtn.setFixedWidth(70)
        self.fromObjectSelectAllBtn.clicked.connect(self.fromObjectSelectAll)
        self.fromObjectSelectAllBtn.setStyleSheet('background-color:' + black)

        # None button select (fromObject)
        self.fromObjectSelectNoneBtn = QtWidgets.QPushButton('None')
        self.fromObjectSelectNoneBtn.setFixedWidth(70)
        self.fromObjectSelectNoneBtn.clicked.connect(self.fromObjectSelectNone)
        self.fromObjectSelectNoneBtn.setStyleSheet('background-color:' + black)

        # Reload button (fromObject)
        self.fromObjectReloadBtn = QtWidgets.QPushButton('Reload')
        self.fromObjectReloadBtn.clicked.connect(self.fromObjectReload)
        self.fromObjectReloadBtn.setStyleSheet('background-color:' + black)



        ### "TO OBJECT" SECTION
        #
        # Caption (toObject)
        self.toObjectLabel = QtWidgets.QLabel("TO ")
        self.toObjectLabel.setFixedHeight(70)
        self.toObjectLabel.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        #self.toObjectLabel.setStyleSheet('background-color:' + white + '; color:' + black)

        # Get selected button (toObject)
        self.toObjectGetSelectedBtn = QtWidgets.QPushButton('Get selected')
        self.toObjectGetSelectedBtn.setStyleSheet('background-color:' + white + '; color:' + black)
        self.toObjectGetSelectedBtn.clicked.connect(self.toObjectGetSelected)
       
        # Filter object type (toObject)
        self.toObjectFilterLabel = QtWidgets.QLabel('Show:')
        self.toObjectFilterVisibleChk = QtWidgets.QCheckBox('Visible nodes only')
        self.toObjectFilterVisibleChk.setChecked(True)
        self.toObjectFilterVisibleChk.setStyleSheet('background-color:' + white + '; color:' + black)
        self.toObjectFilterVisibleChk.stateChanged.connect(self.toObjectReload)
        self.toObjectFilterRefNodesChk = QtWidgets.QCheckBox('Reference nodes only')
        self.toObjectFilterRefNodesChk.setStyleSheet('background-color:' + white + '; color:' + black)
        self.toObjectFilterRefNodesChk.stateChanged.connect(self.toObjectReload)
        self.toObjectFilterTopNodesChk = QtWidgets.QCheckBox('Top nodes only')
        self.toObjectFilterTopNodesChk.setStyleSheet('background-color:' + white + '; color:' + black)
        self.toObjectFilterTopNodesChk.stateChanged.connect(self.toObjectReload)
       
        # SearchBox input for filter list (toObject)
        self.toObjectSearchBox = QtWidgets.QLineEdit('', self)
        self.toObjectRegex = QtCore.QRegExp('[0-9A-Za-z_]+')
        self.toObjectValidator = QtGui.QRegExpValidator(self.toObjectRegex)
        self.toObjectSearchBox.setValidator(self.toObjectValidator)
        self.toObjectSearchBox.textChanged.connect(self.toObjectFilter)
        self.toObjectSearchBox.setStyleSheet('background-color:' + white + '; color:' + black)
        self.toObjectSearchBox.setPlaceholderText("Search...")

        # List of objects (toObject)
        self.toObjectQList = QtWidgets.QListWidget(self)
        self.toObjectQList.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.toObjectQList.setMinimumWidth(150)
        self.toObjectQList.itemSelectionChanged.connect(self.toObjectSel)
        self.toObjectQList.setStyleSheet('background-color:' + white + '; color:' + black)

        self.selecttoObjectLabel = QtWidgets.QLabel('Select')
        
        # All button select (toObject)
        self.toObjectSelectAllBtn = QtWidgets.QPushButton('All')
        self.toObjectSelectAllBtn.setFixedWidth(70)
        self.toObjectSelectAllBtn.clicked.connect(self.toObjectSelectAll)
        self.toObjectSelectAllBtn.setStyleSheet('background-color:' + white + '; color:' + black)

        # None button select (toObject)
        self.toObjectSelectNoneBtn = QtWidgets.QPushButton('None')
        self.toObjectSelectNoneBtn.setFixedWidth(70)
        self.toObjectSelectNoneBtn.clicked.connect(self.toObjectSelectNone)
        self.toObjectSelectNoneBtn.setStyleSheet('background-color:' + white + '; color:' + black)

        # Reload button (toObject)
        self.toObjectSelectReloadBtn = QtWidgets.QPushButton('Reload')
        self.toObjectSelectReloadBtn.clicked.connect(self.toObjectReload)
        self.toObjectSelectReloadBtn.setStyleSheet('background-color:' + white + '; color:' + black)
    
        # Status bar
        self.statusBar = QtWidgets.QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.messageChanged.connect(self.statusChanged)

        # Spacers
        self.spacer1 = QtWidgets.QWidget()
        self.spacer1.setFixedHeight(25)
        self.spacer2 = QtWidgets.QWidget()
        self.spacer2.setFixedHeight(25)
        self.spacer3 = QtWidgets.QWidget()
        self.spacer3.setFixedHeight(25)

        # Match button
        self.matchBtn = QtWidgets.QPushButton('Match')
        self.matchBtn.setMinimumWidth(winWidth)
        self.matchBtn.setFixedHeight(60)
        self.matchBtn.clicked.connect(self.match)
        self.matchBtn.setStyleSheet('background-color:' + magent)

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


        ### Adding all elements to layouts
        #
        layout1A.addWidget(self.fromObjectLabel)
        layout1A.addWidget(self.fromObjectGetSelectedBtn)
        layout1A.addWidget(self.fromObjectSearchBox)
        layout1A.addWidget(self.fromObjectQList)
        layout1A.addWidget(self.fromObjectFilterVisibleChk)
        layout1A.addWidget(self.fromObjectFilterTopNodesChk)
        layout1A.addWidget(self.fromObjectFilterRefNodesChk)
        layout1B.addWidget(self.fromObjectSelectLabel)
        layout1B.addWidget(self.fromObjectSelectAllBtn)
        layout1B.addWidget(self.fromObjectSelectNoneBtn)
        layout1A.addWidget(self.fromObjectReloadBtn)

        layout2A.addWidget(self.toObjectLabel)
        layout2A.addWidget(self.toObjectGetSelectedBtn)
        layout2A.addWidget(self.toObjectSearchBox)
        layout2A.addWidget(self.toObjectQList)
        layout2A.addWidget(self.toObjectFilterVisibleChk)
        layout2A.addWidget(self.toObjectFilterTopNodesChk)
        layout2A.addWidget(self.toObjectFilterRefNodesChk)
        layout2B.addWidget(self.selecttoObjectLabel)
        layout2B.addWidget(self.toObjectSelectAllBtn)
        layout2B.addWidget(self.toObjectSelectNoneBtn)
        layout2A.addWidget(self.toObjectSelectReloadBtn)
        
        col1.addWidget(self.spacer1)
        col2.addWidget(self.spacer2)

        layout3.addWidget(self.matchPositionChk)
        layout3.addWidget(self.matchRotationChk)
        layout3.addWidget(self.matchScaleChk)
        layout4.addWidget(self.matchBtn)



        '''
        |‾‾‾‾‾‾‾‾\______________________________________
        |                                               |
        |   ABOUT TAB                                   |
        |                                               |
                                                      '''
        ### LAYOUT
        # Creating layouts
        aboutLayout = QtWidgets.QHBoxLayout(tab2Layout)  
        layout1 = QtWidgets.QVBoxLayout(alignment=QtCore.Qt.AlignCenter)   
        # Adding layouts
        aboutLayout.addLayout(layout1)


        ### UI ELEMENTS
        self.aboutIcon = QtWidgets.QLabel()
        self.aboutIcon.setPixmap(pixmap)
        self.aboutIcon.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)    
        self.aboutLabel = QtWidgets.QLabel('gzMatchTransforms\nv'+version+'\n'+about+'\n\ngzMatchTransforms is a tool for Maya \nto do match transformations \non multiple objects by paired objects \ngiven a first selection list for the origin objects \nand second selection list to target objects..\n\n')
        self.aboutLabel.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)


         ### ADDING ELEMENTS TO LAYOUT
        layout1.addWidget(self.aboutIcon)
        layout1.addWidget(self.aboutLabel)

       

        ### GLOBAL UI WINDOW
        #
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

    ### UI Settings by Tab
    #
    def onTabChange(self, i): 
        #self.statusBar.showMessage(str(i), 2000)
        if i == 0:
            self.tabs.setStyleSheet('QTabWidget::pane {border: 1px solid' + magent + '; background-color:' + darkgrey2 +'}' 'QTabBar::tab:selected {background-color:' + magent +';}')
        if i == 1:
            self.tabs.setStyleSheet('QTabWidget::pane {border: 1px solid' + magent + '; background-color:' + darkgrey2 +'}' 'QTabBar::tab:selected {background-color:' + magent +';}')


    ### "FROM OBJECT" SECTION
    #
    def fromObjectGetSelected(self):
        selection = cmds.ls(sl=1)
        if len(selection) < 1:
            self.statusBar.showMessage('Must be selected at least one item', 4000)
            self.statusBar.setStyleSheet('background-color:'+red)
        else:
            self.fromObjectQList.clear()
            self.fromObjectQList.addItems(selection)
            self.fromObjectQList.selectAll()

    
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
        dag = 1
        fromObjectTranforms = 1
        global fromObjectList

        if self.fromObjectFilterVisibleChk.isChecked() == True:
            fromObjectVisible = 1
        else:
            fromObjectVisible = 0

        if self.fromObjectFilterRefNodesChk.isChecked() == True:
            fromObjectRefs = 1
        else:
            fromObjectRefs = 0

        if self.fromObjectFilterTopNodesChk.isChecked() == True:
            fromObjectTop = 1
            fromObjectTranforms = 0
            dag = 0
        else:
            fromObjectTop = 0
            fromObjectTranforms = 1
            dag = 1

        fromObjectList = []
        fromObjectList.append(cmds.ls(transforms=fromObjectTranforms, dag=dag, v=fromObjectVisible, rn=fromObjectRefs, assemblies=fromObjectTop))
        
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
        if len(fromObjectSelected) < 1:
            del fromObjectSelected[:]
        self.fromObjectLabel.setText('FROM ')

    
    def fromObjectReload(self):
        self.fromObjectQList.clear()
        if len(fromObjectSelected) < 1:
            del fromObjectSelected[:]
        self.fromObjectLabel.setText('FROM ')
        self.fromObjectLoad()

    

        


    ### "TO OBJECT" SECTION
    #
    def toObjectGetSelected(self):
        selection = cmds.ls(sl=1)
        if len(selection) < 1:
            self.statusBar.showMessage('Must be selected at least one item', 4000)
            self.statusBar.setStyleSheet('background-color:'+red)
        else:
            self.toObjectQList.clear()
            self.toObjectQList.addItems(selection)
            self.toObjectQList.selectAll()

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
        
        if self.toObjectFilterTopNodesChk.isChecked() == True:
            toObjectTop = 1
            toObjectTranforms = 0
            dag = 0
        else:
            toObjectTop = 0
            toObjectTranforms = 1
            dag = 1

        toObjectList = []
        toObjectList.append(cmds.ls(transforms=toObjectTranforms, dag=dag, v=toObjectVisible, rn=toObjectRefs, assemblies=toObjectTop))

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
        if len(toObjectSelected) < 1:
            del toObjectSelected[:]
        self.toObjectLabel.setText('TO ')


    def toObjectReload(self):
        self.toObjectQList.clear()
        if len(toObjectSelected) < 1:
            del toObjectSelected[:]
        self.toObjectLoad()
        self.toObjectLabel.setText('TO ')
        

    
    
    ### MATCH
    def match(self):
        if len(fromObjectSelected) < 1 or len(toObjectSelected) < 1:
            self.statusBar.showMessage('Must be selected at least one item in both lists', 4000)
            self.statusBar.setStyleSheet('background-color:'+red)
        else:           
        
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
                self.statusBar.showMessage('Transforms for '+ str(len(toObjectSelected))+' items matched successfuly!', 4000)
                self.statusBar.setStyleSheet('background-color:'+green)
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
    win = gzMatchTransforms(parent=getMainWindow())
    try:
        win.close()
    except:
        pass
  
    win.show()
    win.raise_()

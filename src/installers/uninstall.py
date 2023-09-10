'''
████████████████████████████████████████████████████████████████████████████
    
    gzMatchTransforms for Maya
    
    Description: gzMatchTransforms is a tool for manage the name of the Maya 
    nodes usually objects in the scene.


    Author: AlbertoGZ
    albertogzonline@gmail.com
    https://github.com/AlbertoGZ-dev

████████████████████████████████ UNINSTALLER ███████████████████████████████  

'''

import os
import sys
import shutil

from os import path, rename, remove, listdir
from time import sleep
from pathlib import Path





homedir = os.path.expanduser('~')
mayaVersions = ['2018', '2019', '2020', '2021', '2022', '2023', '2024']
os = sys.platform
setupFilePath = path.dirname(path.abspath('__file__')) + '/'
scriptName = 'gzMatchTransforms'
scriptIcon = 'gzMatchTransformsIcon.png'
scriptShelf = 'shelf_gzTools.mel'
        


def getOS():
    if os == 'linux' or os == 'linux2':
        # linux
        mayaUserPath = homedir + '/Library/Preferences/Autodesk/maya/'
        if path.exists(mayaUserPath):
            return mayaUserPath
        else:
            print('Maya user path not found')
    elif os == 'darwin':
        # OS X
        mayaUserPath = homedir + '/Library/Preferences/Autodesk/maya/'
        if path.exists(mayaUserPath):
            return mayaUserPath
        else:
            print('Maya user path not found')
    elif os == 'win32':
        # Windows
        mayaUserPath = homedir + '/Documents/maya/'
        if path.exists(mayaUserPath):
            return mayaUserPath
        else:
            print('Maya user path not found')
        


def uninstall(): 
    mayaUserPath = getOS()

    # Get only the installed versions of Maya
    listMayaUserPath = listdir(mayaUserPath)
    installedMayas = set(listMayaUserPath).intersection(mayaVersions)

    for currentVersion in installedMayas:

        mayaScriptsPath = []
        mayaScriptsPath.append(mayaUserPath + currentVersion + '/scripts/')
        
        mayaShelvesPath = []
        mayaShelvesPath.append(mayaUserPath + currentVersion + '/prefs/shelves/')
        
        mayaIconsPath = []
        mayaIconsPath.append(mayaUserPath + currentVersion + '/prefs/icons/')
       
        # Remove/Restore shelf  
        for shelf in mayaShelvesPath:        
            if path.exists(shelf):
                if path.isfile(shelf + scriptShelf) and path.isfile(shelf + scriptShelf + '.bak'):
                    # Restore original file
                    rename(shelf + scriptShelf,            shelf + scriptShelf + '.tmp')
                    rename(shelf + scriptShelf + '.bak',   shelf + scriptShelf)
                    rename(shelf + scriptShelf + '.tmp',   shelf + scriptShelf + '.bak')
                    
                    print('Removing ' + scriptName + ' button from Maya ' + currentVersion + ' shelf...')
                    sleep(0.3)
                    print('[ SUCCESSFULLY ]\n' )
                else:
                    print("Not found shelf file")

        
        # Remove icon  
        for icon in mayaIconsPath:        
            if path.exists(icon):
                if path.isfile(icon + scriptIcon):
                    # Remove icon from Maya icons default folder
                    remove(icon + scriptIcon)
                    print('Removing ' + scriptIcon + ' from ' + mayaUserPath + currentVersion + '/prefs/icons/')
                    sleep(0.3)
                    print('[ SUCCESSFULLY ]\n' )
                else:
                    print("Not found icon file")

                
        # Remove script folder     
        for p in mayaScriptsPath:        
            if path.exists(p):
                target = p + '/' + scriptName + '/'
                shutil.rmtree(target, ignore_errors=True)
                
                # Uninstall completed
                print('█████████████████████████████████████████████████████████████████████████████████')
                print('██                                                                             ██')
                print('██           '+scriptName+' uninstalled successfully for Maya '+currentVersion+'!         ██')
                print('██                                                                             ██')
                print('█████████████████████████████████████████████████████████████████████████████████')
                print('\n')
                sleep(1)
            else:
                print('[ FAILED ]\n' )
                


   
getOS()
uninstall()
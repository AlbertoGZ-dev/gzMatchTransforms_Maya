'''
████████████████████████████████████████████████████████████████████████████
    
    gzMatchTransforms for Maya
    
    Description: gzMatchTransforms is a tool for manage the name of the Maya 
    nodes usually objects in the scene.


    Author: AlbertoGZ
    albertogzonline@gmail.com
    https://github.com/AlbertoGZ-dev

██████████████████████████████ INSTALLER ███████████████████████████████████

'''

import os
import sys
import shutil
import re

from os import path, unlink, rename, listdir
from distutils.dir_util import copy_tree
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
        


def install():
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

        # Copy contents to destination 
        print(Path('Copying gzMatchTransforms to ' + mayaUserPath + currentVersion + '/scripts/gzMatchTransforms/ ...' ))
        sleep(0.2)

        for p in mayaScriptsPath:        
            if path.exists(p):
                src = setupFilePath + '/src/'
                target = p + '/' + scriptName + '/'
                copy_tree(src, target)
                sleep(0.5)
                
                print('[ SUCCESSFULLY ]\n' )
            else:
                print('[ FAILED ]\n' )


        
        
        # Creating button in shelves.
        gzToolsShelfSrcPath = 'src/installers/'
        gzToolsShelf = gzToolsShelfSrcPath + scriptShelf

        print('Adding ' + scriptName + ' button to Maya ' + currentVersion + ' shelf ...')
        sleep(0.5) 

        for mayaShelfPath in mayaShelvesPath:        
            
            if path.exists(mayaShelfPath):
                if path.isfile(mayaShelfPath + scriptShelf):
                    print ('gzTools shelf already exists')
                     
                    file1 = mayaShelfPath + scriptShelf
                    file2 = setupFilePath + 'src/installers/shelf_Icon.mel'
                    file3 = mayaShelfPath + scriptShelf + '.tmp'

                    # Backup shelf_gzTools.mel
                    shutil.copy(file1, file1 + '.bak')

                    # Append config text to file
                    filenames = [file1, file2]
                    with open(file3, 'w') as outfile:
                        for fname in filenames:
                            with open(fname) as infile:
                                outfile.write(infile.read())


                    # Remove first closure bracket to sanity code
                    # Read in the file
                    with open(file3, 'r') as file :
                        filedata = file.read()
                        #file.close()
                    
                    # Remove existent button
                    #filedata = re.sub('//begins_gzMatchTransforms?(.*?)//ends_gzMatchTransforms', '', filedata, flags=re.DOTALL)


                    # Replace the target string
                    filedata = filedata.replace('}', '', 1)

                    # Write the file out again
                    with open(file3, 'w') as file:
                        file.write(filedata)
                        #file.close()

                    # Restore original name
                    unlink(file1)
                    rename(file3, file1)
                    
                else:
                    # Creating gzTools shelf
                    print ('Creating gzTools shelf ...')
                    shutil.copy(gzToolsShelf,  mayaShelfPath)
                    sleep(0.3)
                    print('[ SUCCESSFULLY ]\n' )
            
            else:
                print('[ FAILED ]\n' )
            


            # Copy icon to Maya icons default folder
            iconSrc = setupFilePath + 'src/icons/' + scriptIcon
            iconTarget = mayaUserPath + currentVersion + '/prefs/icons/' + scriptIcon
            shutil.copy(iconSrc, iconTarget)
            sleep(0.5)

            print('[ SUCCESSFULLY ]\n' )
            


            # Installation completed
            print('█████████████████████████████████████████████████████████████████████████████████')
            print('██                                                                             ██')
            print('██           '+scriptName+' installed successfully for Maya '+currentVersion+'!           ██')
            print('██                                                                             ██')
            print('█████████████████████████████████████████████████████████████████████████████████')
            sleep(1)

   
getOS()
install()
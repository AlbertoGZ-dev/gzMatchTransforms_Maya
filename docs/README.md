# gzMatchTransforms for Maya
gzMatchTransforms is a tool for Maya to do match transformations on multiple objects by paired objects given a first selection list for the origin objects and second selection list to target objects. 

<img src="https://github.com/AlbertoGZ-dev/gzMatchTransforms/blob/master/gzMatchTransforms.jpg"></img>

## Setup

#### Automatic installation

Run the installer for your plattform.

- Windows by double clicking *install_win.bat* file.
- MacOS by double clicking *install_mac* file.
- Linux open shell and execute *install_linux.sh* file.

Note: on MacOS and Linux you may need to set execution permissions the installer file. Ex. *chmod +x install_linux.sh*


#### Manual installation

Place the *gzMatchTransforms.py* and *\_\_init\_\_.py* files in a folder named *gzMatchTransforms* in your Maya scripts directory and create a python shell button with the following code:

```python
from gzMatchTransforms import gzMatchTransforms

try:
    md_win.close()
except:
    pass
md_win = gzMatchTransforms.gzMatchTransforms(parent=gzMatchTransforms.getMainWindow())
md_win.show()
md_win.raise_()
```

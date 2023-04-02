# Match MultiObject
Match MultiObject makes match transformations on multiple objects by paired objects given a first selection list for the origin objects and second selection list to target objects. 

<img src="https://github.com/AlbertoGZ-dev/matchMultiObject/blob/main/matchMultiObject.jpg"></img>

## Setup

#### Manual installation

Place the *matchMultiObject.py* and *\_\_init\_\_.py* files in a folder named *matchMultiObject* in your Maya scripts directory and create a python shell button with the following code:

```python
from matchMultiObject import matchMultiObject

try:
    md_win.close()
except:
    pass
md_win = matchMultiObject.matchMultiObject(parent=matchMultiObject.getMainWindow())
md_win.show()
md_win.raise_()
```

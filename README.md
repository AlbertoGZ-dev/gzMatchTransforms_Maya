# Character Toolset
Character Toolset is a tool to automatize some repetitive tasks in character preparation Maya scene for CrimsonSky.

<img src="https://github.com/AlbertoGZ-dev/characterToolset/blob/main/characterToolset.jpg"></img>

## Setup

#### Manual installation

Place the *characterToolset.py* and *\_\_init\_\_.py* files in a folder named *characterToolset* in your Maya scripts directory and create a python shell button with the following code:

```python
from characterToolset import characterToolset

try:
    md_win.close()
except:
    pass
md_win = characterToolset.characterToolset(parent=characterToolset.getMainWindow())
md_win.show()
md_win.raise_()
```

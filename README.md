# volume-control-by-hand
* ### Works on MacOS, Windows, Linux


## Install on MacOS
```
pip install --upgrade mediapipe osascript
```

## Install on Windows
```
pip install --upgrade mediapipe osascript comtypes pycaw
```

## Install on Linux
```
sudo apt -y install python3-pip python3-alsaaudio
pip install --upgrade mediapipe
```


## Known issues

### If you have this problem on Windows
```
Traceback (most recent call last):
  File "C:\Users\tuxta\OneDrive\Desktop\volume-control\main.py", line 2, in <module>
    from mediapipe import solutions
  File "C:\Users\tuxta\AppData\Local\Programs\Python\Python310\lib\site-packages\mediapipe\__init__.py", line 15, in <module>
    from mediapipe.python import *
  File "C:\Users\tuxta\AppData\Local\Programs\Python\Python310\lib\site-packages\mediapipe\python\__init__.py", line 17, in <module>
    from mediapipe.python._framework_bindings import resource_util
ImportError: DLL load failed while importing _framework_bindings: The specified module could not be found.
```
### Run this command
```
pip install --upgrade msvc-runtime
```

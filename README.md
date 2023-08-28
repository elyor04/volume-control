# volume-control-by-hand
* ### Works on MacOS, Windows and Linux


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
  File "C:\Users\username\OneDrive\Desktop\volume-control\main.py", line 2, in <module>
    from mediapipe import solutions
  File "C:\Users\username\AppData\Local\Programs\Python\Python310\lib\site-packages\mediapipe\__init__.py", line 15, in <module>
    from mediapipe.python import *
  File "C:\Users\username\AppData\Local\Programs\Python\Python310\lib\site-packages\mediapipe\python\__init__.py", line 17, in <module>
    from mediapipe.python._framework_bindings import resource_util
ImportError: DLL load failed while importing _framework_bindings: The specified module could not be found.
```
### Run this command
```
pip install --upgrade msvc-runtime
```


```python
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume

class Volume:
    def __init__(self):
        self.devices = AudioUtilities.GetSpeakers()
        self.interface = self.devices.Activate(ISimpleAudioVolume._iid_, 1, None)
        self.volume = self.interface.QueryInterface(ISimpleAudioVolume)

    def set_volume(self, level):
        # level should be between 0.0 and 1.0
        self.volume.SetMasterVolume(level, None)

    def get_volume(self):
        return self.volume.GetMasterVolume()


v = Volume()
v.set_volume(0.5)  # set volume to 50%
print(v.get_volume())  # Output: 0.5
```

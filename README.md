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
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import numpy as np

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

desired_vol = 50

vol_range = volume.GetVolumeRange()
min_vol = vol_range[0]
max_vol = vol_range[1]

desired_vol_db = np.interp(desired_vol, [0, 100], [min_vol, max_vol])
volume.SetMasterVolumeLevelScalar(desired_vol / 100, None)

curr_vol = round(volume.GetMasterVolumeLevelScalar() * 100)
print(f'Volume set to: {int(curr_vol)} %')
```

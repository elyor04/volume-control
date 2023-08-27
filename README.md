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
cap = cv.VideoCapture("http://192.168.0.100:8080/video")
vol = VolumeController()
hands = mp_hands.Hands(max_num_hands=2, model_complexity=0)

wd, hg = int(cap.get(3) * 0.5), int(cap.get(4) * 0.5)
checker, percents = True, []
last_perc = 0

while True:
    success, image = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue
    image = cv.flip(cv.resize(image, None, fx=0.5, fy=0.5, interpolation=cv.INTER_AREA), 1)
```

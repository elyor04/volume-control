import cv2 as cv
from mediapipe import solutions
from math import hypot
from platform import system
from threading import Timer
from typing import Union

platform = system().lower().strip()

if platform == "darwin":
    from osascript import osascript

    class AudioController:
        def __init__(self) -> None:
            pass

        def setVolume(self, volume: int, volType: str = "output") -> None:
            """volType: output, input, alert"""
            osascript(f"set volume {volType} volume {volume}")

        def getVolume(self, volType: str = "output") -> int:
            """volType: output, input, alert"""
            volChoose = {"output": 0, "input": 1, "alert": 2}
            result = osascript("get volume settings")
            volume = (
                result[1]
                .split(",")[volChoose[volType]]
                .replace(f"{volType} volume:", "")
            )
            return int(volume)

elif platform == "windows":
    from ctypes import POINTER, cast
    from comtypes import CLSCTX_ALL
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

    class AudioController:
        def __init__(self) -> None:
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)

            self.volume = cast(interface, POINTER(IAudioEndpointVolume))
            self.vol_vals = self._getRange(*self.volume.GetVolumeRange())
            self._val_n = len(self.vol_vals) - 1

        def _getRange(self, r1: float, r2: float, r3: float) -> list:
            r_lst = list()
            while r1 <= r2:
                r_lst.append(r1)
                r1 += r3
            return r_lst

        def getVolume(self) -> float:
            return self.volume.GetMasterVolumeLevel()

        def setVolume(self, vol_index: int = None, vol_val: float = None) -> None:
            if vol_index is not None:
                vol_val = self.vol_vals[min(vol_index, self._val_n - 5)]
            self.volume.SetMasterVolumeLevel(vol_val, None)

elif platform == "linux":
    pass

mp_drawing = solutions.drawing_utils
mp_drawing_styles = solutions.drawing_styles
mp_hands = solutions.hands
CoordinateOrNone = Union[tuple[int, int], None]


def getPercent(
    cords: list, im_wd: int, im_hg: int
) -> tuple[int, CoordinateOrNone, CoordinateOrNone]:
    x1, y1, z1 = cords[-1][4]
    x2, y2, z2 = cords[-1][8]
    f_cord = cords[-1][5:9]
    f_cord = [(f_cord[i], f_cord[i + 1]) for i in range(len(f_cord) - 1)]

    percent = round(hypot((x1 - x2), (y1 - y2), (z1 - z2)), 4)
    f_len = sum(
        [
            round(hypot((x1 - x2), (y1 - y2), (z1 - z2)), 4)
            for ((x1, y1, z1), (x2, y2, z2)) in f_cord
        ]
    )
    percent = min(int((percent / f_len) * 60), 100)

    pt1 = mp_drawing._normalized_to_pixel_coordinates(x1, y1, im_wd, im_hg)
    pt2 = mp_drawing._normalized_to_pixel_coordinates(x2, y2, im_wd, im_hg)
    return (percent, pt1, pt2)


def setCheckerTrue() -> None:
    global checker
    checker = True


cap = cv.VideoCapture(0)
aud = AudioController()
hands = mp_hands.Hands(max_num_hands=2, model_complexity=0)

wd, hg = int(cap.get(3)), int(cap.get(4))
checker, percents = True, []
last_perc = 0

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue
    image = cv.flip(image, 1)

    image.flags.writeable = False
    image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    results = hands.process(image)

    image.flags.writeable = True
    image = cv.cvtColor(image, cv.COLOR_RGB2BGR)
    hand_landmarks = results.multi_hand_landmarks

    if hand_landmarks:
        coordinates = [
            [(land.x, land.y, land.z) for land in lands.landmark]
            for lands in hand_landmarks
        ]
        percent, pt1, pt2 = getPercent(coordinates, wd, hg)
        percents.insert(0, percent)
        for landmarks in hand_landmarks:
            mp_drawing.draw_landmarks(image, landmarks, mp_hands.HAND_CONNECTIONS)

    if hand_landmarks:
        cv.putText(
            image,
            f"{percent}",
            (5, 20),
            cv.FONT_HERSHEY_COMPLEX_SMALL,
            1.0,
            (255, 0, 0),
            1,
        )
        if pt1 and pt2:
            cv.line(image, pt1, pt2, (255, 0, 0), 3)

        if checker and (len(percents) >= 5):
            percents = percents[:5]
            percent = sum(percents) // 5
            if percent != last_perc:
                aud.setVolume(percent)
                last_perc = percent
            checker = False
            _tm = Timer(0.1, setCheckerTrue)
            _tm.start()

    cv.imshow("Hand Control", image)
    if cv.waitKey(2) == 27:  # esc
        break

cap.release()
cv.destroyAllWindows()

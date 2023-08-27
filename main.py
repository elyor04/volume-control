from cv2 import (
    VideoCapture,
    FONT_HERSHEY_COMPLEX_SMALL,
    COLOR_BGR2RGB,
    COLOR_RGB2BGR,
    cvtColor,
    putText,
    imshow,
    flip,
    line,
    waitKey,
    destroyAllWindows,
)
from mediapipe import solutions
from math import hypot
from osascript import osascript
from threading import Timer
from typing import Union

mp_drawing = solutions.drawing_utils
mp_drawing_styles = solutions.drawing_styles
mp_hands = solutions.hands
CoordinateOrNone = Union[tuple[int, int], None]


class AudioController:
    @classmethod
    def setVolume(volume: int, volType: str = "output") -> None:
        """volType: output, input, alert"""
        osascript(f"set volume {volType} volume {volume}")

    @classmethod
    def getVolume(volType: str = "output") -> int:
        """volType: output, input, alert"""
        volChoose = {"output": 0, "input": 1, "alert": 2}
        result = osascript("get volume settings")
        volume = (
            result[1].split(",")[volChoose[volType]].replace(f"{volType} volume:", "")
        )
        return int(volume)


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


cap = VideoCapture(0)
hands = mp_hands.Hands(max_num_hands=2, model_complexity=0)
wd, hg = int(cap.get(3)), int(cap.get(4))
checker, percents = True, []
last_perc = 0

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue
    image = flip(image, 1)

    image.flags.writeable = False
    image = cvtColor(image, COLOR_BGR2RGB)
    results = hands.process(image)

    image.flags.writeable = True
    image = cvtColor(image, COLOR_RGB2BGR)
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
        putText(
            image,
            f"{percent}",
            (5, 20),
            FONT_HERSHEY_COMPLEX_SMALL,
            1.0,
            (255, 0, 0),
            1,
        )
        if pt1 and pt2:
            line(image, pt1, pt2, (255, 0, 0), 3)

        if checker and (len(percents) >= 5):
            percents = percents[:5]
            percent = sum(percents) // 5
            if percent != last_perc:
                AudioController.setVolume(percent)
                last_perc = percent
            checker = False
            _tm = Timer(0.1, setCheckerTrue)
            _tm.start()

    imshow("Hand Control", image)
    if waitKey(4) == 27:
        cap.release()
        destroyAllWindows()
        break

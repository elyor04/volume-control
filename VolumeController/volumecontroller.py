from platform import system
from re import search

platform = system().lower().strip()

if platform == "darwin":
    from osascript import osascript

    class VolumeController:
        def __init__(self) -> None:
            pass

        def setVolume(self, volume: int) -> None:
            osascript(f"set volume output volume {volume}")

        def getVolume(self) -> int:
            result = osascript("get volume settings")[1]
            result = search("output volume:([0-9]+)", result)
            return int(result.groups()[0])

elif platform == "windows":
    from ctypes import POINTER, cast
    from comtypes import CLSCTX_ALL
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

    class VolumeController:
        def __init__(self) -> None:
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            self.device = cast(interface, POINTER(IAudioEndpointVolume))

        def setVolume(self, volume: int) -> None:
            volume /= 100
            self.device.SetMasterVolumeLevelScalar(volume, None)

        def getVolume(self) -> int:
            volume = self.device.GetMasterVolumeLevelScalar()
            return round(volume * 100)

elif platform == "linux":
    from alsaaudio import Mixer

    class VolumeController:
        def __init__(self) -> None:
            self.device = Mixer()

        def setVolume(self, volume: int) -> None:
            self.device.setvolume(volume)

        def getVolume(self) -> int:
            return self.device.getvolume()[0]

else:
    print("This platform is not supported")
    exit(0)

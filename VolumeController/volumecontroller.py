from platform import system

platform = system().lower().strip()

if platform == "darwin":
    from osascript import osascript

    class VolumeController:
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

    class VolumeController:
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

        def setVolume(self, vol_index: int = None, vol_val: float = None) -> None:
            if vol_index is not None:
                vol_val = self.vol_vals[min(vol_index, self._val_n - 5)]
            self.volume.SetMasterVolumeLevel(vol_val, None)

        def getVolume(self) -> float:
            return self.volume.GetMasterVolumeLevel()

elif platform == "linux":
    from alsaaudio import Mixer

    class VolumeController:
        def __init__(self) -> None:
            self.volume = Mixer()

        def setVolume(self, volume: int) -> None:
            self.volume.setvolume(volume)

        def getVolume(self) -> int:
            return self.volume.getvolume()[0]

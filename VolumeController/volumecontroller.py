from platform import system

platform = system().lower().strip()

if platform == "darwin":
    from osascript import osascript

    class VolumeController:
        def __init__(self) -> None:
            pass

        def setVolume(self, volume: int) -> None:
            """volType: output, input, alert"""
            osascript(f"set volume output volume {volume}")

        def getVolume(self) -> int:
            """volType: output, input, alert"""
            volChoose = {"output": 0, "input": 1, "alert": 2}
            result = osascript("get volume settings")
            volume = (
                result[1].split(",")[volChoose["output"]].replace(f"output volume:", "")
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
            self.device = cast(interface, POINTER(IAudioEndpointVolume))
            self.volumes = self._range(*self.device.GetVolumeRange())

        def _range(self, r1: float, r2: float, r3: float) -> list:
            rList = list()
            while r1 <= r2:
                rList.append(r1)
                r1 += r3
            return rList

        def setVolume(self, volume: int) -> None:
            volume = int(len(self.volumes) / 100 * volume)
            volume = max(min(volume, len(self.volumes) - 1), 0)
            self.device.SetMasterVolumeLevel(self.volumes[volume], None)

        def getVolume(self) -> int:
            volume = self.volumes.index(self.device.GetMasterVolumeLevel())
            volume = int(100 / len(self.volumes) * volume)
            return max(min(volume, 100), 0)

elif platform == "linux":
    from alsaaudio import Mixer

    class VolumeController:
        def __init__(self) -> None:
            self.device = Mixer()

        def setVolume(self, volume: int) -> None:
            self.device.setvolume(volume)

        def getVolume(self) -> int:
            return self.device.getvolume()[0]

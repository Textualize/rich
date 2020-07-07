import sys

from dataclasses import dataclass


@dataclass
class WindowsConsoleFeatures:
    """Windows features available."""

    vt: bool
    truecolor: bool


try:
    import ctypes
    from ctypes import wintypes
    from ctypes import LibraryLoader

    windll = LibraryLoader(ctypes.WinDLL)
except (AttributeError, ImportError):

    # Fallback if we can't load the Windows DLL
    def get_windows_console_features() -> WindowsConsoleFeatures:
        features = WindowsConsoleFeatures()
        return features


else:

    STDOUT = -11
    ENABLE_VIRTUAL_TERMINAL_PROCESSING = 4
    _GetConsoleMode = windll.kernel32.GetConsoleMode
    _GetConsoleMode.argtypes = [wintypes.HANDLE, wintypes.LPDWORD]
    _GetConsoleMode.restype = wintypes.BOOL

    _GetStdHandle = windll.kernel32.GetStdHandle
    _GetStdHandle.argtypes = [
        wintypes.DWORD,
    ]
    _GetStdHandle.restype = wintypes.HANDLE

    def get_windows_console_features() -> WindowsConsoleFeatures:
        """Get windows console fatures.

        Returns:
            WindowsConsoleFeatures: An instance of WindowsConsoleFeatures.
        """
        handle = _GetStdHandle(STDOUT)
        console_mode = wintypes.DWORD()
        result = _GetConsoleMode(handle, console_mode)
        vt = bool(result and console_mode.value & ENABLE_VIRTUAL_TERMINAL_PROCESSING)
        truecolor = False
        if vt:
            win_version = sys.getwindowsversion()
            truecolor = win_version.major > 10 or (
                win_version.major == 10 and win_version.build > 15063
            )
        features = WindowsConsoleFeatures(vt=vt, truecolor=truecolor)
        return features


if __name__ == "__main__":
    print(get_windows_console_features())


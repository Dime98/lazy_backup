# claude code snippet
import ctypes
from ctypes import wintypes
from pathlib import Path


def _ns_to_filetime(ns: int) -> wintypes.FILETIME:
    # FILETIME = 100ns ticks since 1601-01-01; Unix epoch offset below
    ticks = ns // 100 + 116444736000000000
    return wintypes.FILETIME(ticks & 0xFFFFFFFF, ticks >> 32)


# --- Win32 setup -----------------------------------------------------------
_kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)

_kernel32.CreateFileW.argtypes = [
    wintypes.LPCWSTR,
    wintypes.DWORD,
    wintypes.DWORD,
    wintypes.LPVOID,
    wintypes.DWORD,
    wintypes.DWORD,
    wintypes.HANDLE,
]
_kernel32.CreateFileW.restype = wintypes.HANDLE

_kernel32.SetFileTime.argtypes = [
    wintypes.HANDLE,
    ctypes.POINTER(wintypes.FILETIME),
    ctypes.POINTER(wintypes.FILETIME),
    ctypes.POINTER(wintypes.FILETIME),
]
_kernel32.SetFileTime.restype = wintypes.BOOL

_kernel32.CloseHandle.argtypes = [wintypes.HANDLE]
_kernel32.CloseHandle.restype = wintypes.BOOL

FILE_WRITE_ATTRIBUTES = 0x0100
FILE_SHARE_ALL = 0x1 | 0x2 | 0x4
OPEN_EXISTING = 3
FILE_FLAG_BACKUP_SEMANTICS = 0x02000000
FILE_FLAG_OPEN_REPARSE_POINT = 0x00200000  # operate on the link, not the target
INVALID_HANDLE_VALUE = wintypes.HANDLE(-1).value


def set_link_times(path: Path, ns: int):
    """Set creation, access and modified time of the link itself."""
    handle = _kernel32.CreateFileW(
        str(path),
        FILE_WRITE_ATTRIBUTES,
        FILE_SHARE_ALL,
        None,
        OPEN_EXISTING,
        FILE_FLAG_OPEN_REPARSE_POINT | FILE_FLAG_BACKUP_SEMANTICS,
        None,
    )
    if handle == INVALID_HANDLE_VALUE:
        raise ctypes.WinError(ctypes.get_last_error())
    try:
        ft = _ns_to_filetime(ns)
        if not _kernel32.SetFileTime(
            handle, ctypes.byref(ft), ctypes.byref(ft), ctypes.byref(ft)
        ):
            raise ctypes.WinError(ctypes.get_last_error())
    finally:
        _kernel32.CloseHandle(handle)

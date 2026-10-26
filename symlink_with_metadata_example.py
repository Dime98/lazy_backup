import os
import sys


IS_WINDOWS = sys.platform == "win32"
if IS_WINDOWS:
    from make_windows_symlink import set_link_times


def example(
    source_file,
    destination_file,
):
    destination_file.symlink_to(source_file)
    source_stat = source_file.stat()
    if IS_WINDOWS:
        set_link_times(destination_file, source_stat.st_mtime_ns)
    else:
        os.utime(
            destination_file,
            ns=(source_stat.st_atime_ns, source_stat.st_mtime_ns),
            follow_symlinks=False,
        )

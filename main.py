import datetime
import os
import shutil
from pathlib import Path

from color_prints import prGreen, prPurple, prCyan, prRed


# modification date, human-readable
def _get_modification_date(file):
    t = os.path.getmtime(file)
    return datetime.datetime.fromtimestamp(t)


def get_modification_date(file: Path):
    return file.stat().st_mtime


def get_file_names_by_type(folder: Path, file_type: list | str) -> dict:
    file_candidates = {}
    for file in folder.iterdir():
        if file_type != "*" and file.suffix.casefold() not in file_type:
            continue
        file_candidates[file.name] = {
            "full_path": file,
            "modification_date": get_modification_date(file),
        }
    return file_candidates


def lazy_backup(source_folder: Path, backup_folder: Path, target_file_types: list[str]):
    if not source_folder.exists():
        raise FileNotFoundError(f"'{source_folder}' does not exist.")

    if not backup_folder.exists():
        print(f"Creating backup folder at '{backup_folder}'\n")
        backup_folder.mkdir()

    source_files = get_file_names_by_type(source_folder, target_file_types)
    backup_files = get_file_names_by_type(backup_folder, "*")

    print(f"{source_folder=}, found {len(source_files)} file(s).")
    print(f"{backup_folder=}, found {len(backup_files)} file(s).")
    print(f"{target_file_types=}")

    files_to_copy = list(set(source_files) - set(backup_files))
    files_to_delete = list(set(backup_files) - set(source_files))

    print(f"\n -- Copying {len(files_to_copy)} file(s)")
    for file in files_to_copy:
        prGreen(f"\t copying {file} ")
        source_file = source_folder / file
        destination_file = backup_folder / file
        try:
            shutil.copy2(source_file, destination_file)
        except Exception as e:
            prRed(f"Could not copy '{source_file}'.\n{e}")
            return

    print(f"\n -- Deleting {len(files_to_delete)} file(s)")
    for file in files_to_delete:
        prPurple(f"\t Deleting {file}")
        file_path = backup_folder / file
        file_path.unlink(missing_ok=True)

    assert len(get_file_names_by_type(source_folder, target_file_types)) == len(
        get_file_names_by_type(backup_folder, target_file_types)
    ), "Number of files differ in source and backup folders."

    print("\n -- Copying file(s) with different modification date")
    for file in source_files:
        source_file_date = source_files[file].get("modification_date")
        backup_file_date = get_modification_date(backup_folder / file)
        if source_file_date == backup_file_date:
            continue

        prCyan(f"\t Modification date mismatch for {file} ")
        source_file = source_folder / file
        destination_file = backup_folder / file
        shutil.copy2(source_file, destination_file)

    print("\n" + "=" * 80)


def open_folder_timer(folder_to_open: Path, time_to_elapse: int):
    import time
    import threading
    import msvcrt

    print(f"\n'{folder_to_open}' will be opened in {time_to_elapse} seconds")
    print("Press 'enter' to open now, 'x' to exit.")

    action = None
    stop_event = threading.Event()

    def stopwatch(time_to_elapse):
        start = time.time()

        while not stop_event.is_set():
            elapsed = time.time() - start

            if elapsed >= time_to_elapse:
                print("\ntime elapsed, exiting...")
                stop_event.set()
                return

            print(f"\rElapsed: {elapsed:.1f}s", end="")
            time.sleep(0.1)

    def keyboard_listener():
        nonlocal action

        while not stop_event.is_set():
            if msvcrt.kbhit():
                key = msvcrt.getwch()

                if key == "\r":
                    action = "open"
                    stop_event.set()
                    return

                if key.lower() == "x":
                    action = "exit"
                    stop_event.set()
                    return

            time.sleep(0.05)

    timer_thread = threading.Thread(target=stopwatch, args=(time_to_elapse,))
    keyboard_thread = threading.Thread(target=keyboard_listener)

    timer_thread.start()
    keyboard_thread.start()
    stop_event.wait()

    if action == "open":
        print(f"Opening '{folder_to_open}'")
        os.startfile(folder_to_open)

    elif action == "exit":
        print("Closing application.")

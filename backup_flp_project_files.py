from pathlib import Path
from main import lazy_backup, open_folder_timer


def main():
    fl_file_type = [".flp"]
    audio_file_type = [".wav", ".mp3"]

    fl_source = r"D:/DAW/FL Studio/Data/Projects"
    fl_backup = r"D:/automatedBackUp/Project/Flp"

    recorded_source = r"D:/DAW/FL Studio/user_data/FL Studio/Audio/Recorded"
    recorded_backup = r"D:/automatedBackUp/Project/Recorded"

    rendered_source = r"D:/DAW/FL Studio/user_data/FL Studio/Audio/Rendered"
    rendered_backup = r"D:/automatedBackUp/Project/Rendered"

    sliced_beats_source = r"D:/DAW/FL Studio/Data/Patches/Sliced beats"
    sliced_beats_backup = r"D:/automatedBackUp/Project/Sliced beats"

    template_path = r"D:/DAW/FL Studio/Data/Templates"
    template_backup = r"D:/automatedBackUp/Project/Templates"

    datum = [
        [fl_source, fl_backup, fl_file_type],
        [recorded_source, recorded_backup, audio_file_type],
        [rendered_source, rendered_backup, audio_file_type],
        [sliced_beats_source, sliced_beats_backup, audio_file_type],
        [template_path, template_backup, fl_file_type],
    ]

    for source_folder, backup_folder, target_file_types in datum:
        lazy_backup(
            source_folder=Path(source_folder),
            backup_folder=Path(backup_folder),
            target_file_types=target_file_types,
            use_symlink=False,
        )

    open_folder_timer(folder_to_open=Path(fl_backup), time_to_elapse=5)


if __name__ == "__main__":
    main()

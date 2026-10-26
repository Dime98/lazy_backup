from pathlib import Path
from main import lazy_backup, open_folder_timer


def main():
    audio_file_type = [".wav"]

    audio_files_source = r"D:/DAW/FL Studio/Data/Projects"
    audio_files_backup = "D:/automatedBackUp/wav/wav"

    lazy_backup(
        source_folder=Path(audio_files_source),
        backup_folder=Path(audio_files_backup),
        target_file_types=audio_file_type,
        use_symlink=True,
    )

    open_folder_timer(folder_to_open=Path(audio_files_backup), time_to_elapse=5)


if __name__ == "__main__":
    main()

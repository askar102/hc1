import time
import logging
from pathlib import Path

from watchdog.observers import Observer
from watchdog.events import DirCreatedEvent, FileCreatedEvent, RegexMatchingEventHandler

try:
    import yolo_source.face_handler as face_handler
except ModuleNotFoundError:
    import face_handler


class NewPhotoHandler(RegexMatchingEventHandler):
    def __init__(self, save_dir_path: str, logger):
        super().__init__(regexes=[r'.+\.jpg$'], ignore_directories=True)
        self._save_dir_path: str = save_dir_path
        self._logger = logger

    def on_created(self, event: DirCreatedEvent | FileCreatedEvent) -> None:
        file_stem = Path(event.src_path).stem

        self._logger.info(f"[WATCHER] Found {file_stem}.jpg, making crop...")
        time.sleep(5)

        face_handler.make_crop(
            source_img_path=event.src_path,
            save_dir_path=self._save_dir_path,
            save_filename=f"{file_stem}_crop.jpg",
            remove_tmp=False
        )

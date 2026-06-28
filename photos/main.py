from dl_source.pinterest_dl import download_board
from yolo_source.face_handler import make_dir_watcher
import logging
import multiprocessing

# Короче реализовтаь хуйню, сделать чтобы даунлоадер сам кидал сигнал ватчдогу шо пора
# сканить дирикторию

# Скорее всего здесь баг: так как логер общий, он блокирут поток. FIXME

if __name__ == "__main__":
    log_level = logging.INFO
    logging.basicConfig(level=log_level, format='[%(asctime)s] %(levelname)s: %(message)s', datefmt='%I:%M:%S')

    pin_dl = multiprocessing.Process(
        target=download_board,
        kwargs={
            "board_url": "https://ru.pinterest.com/askar0704/alya/",
            "download_folder": "./static/"
        },
        daemon=True
    )

    pin_dl.start()

    watcher = multiprocessing.Process(
        target=make_dir_watcher,
        kwargs={    
            "watch_dir_path": "./static/",
            "save_dir_path": "./save/"
        },
        daemon=True
    )

    watcher.start()

    pin_dl.join()
    watcher.join()

    # download_board(board_url="https://ru.pinterest.com/askar0704/alya/", download_folder="./static/")
    # make_dir_watcher(watch_dir_path="./test/", save_dir_path="./save/")
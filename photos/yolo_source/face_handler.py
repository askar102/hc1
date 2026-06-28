import os
import cv2
import logging
import shutil
import time

from pathlib import Path

from ultralytics import YOLO
from ultralytics import solutions
from PIL import Image

from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

import numpy as np

try:
    import yolo_source.file_watcher as file_watcher
except ModuleNotFoundError:
    import file_watcher

logger = logging.getLogger(__name__)

def make_crop(source_img_path: str, save_dir_path: str, save_filename: str, save_detections=True, verbose=True, remove_tmp=True) -> None:
    IMAGE_PADDING = 30

    # Turn off logger if not verbose
    if not verbose:
        logger.disabled = True

    if not os.path.isfile(source_img_path):
        logger.warning(f"Cannot find {source_img_path} or it is not a file!")
        logger.warning(f"Please use the make_dir_crop() function for directories.")
        return

    model = YOLO("../yolov8x6_animeface.pt")
    results = model.predict(
        source=source_img_path,
        conf=0.5,
        verbose=verbose
    )

    # Initialization
    source_image = cv2.imread(source_img_path)
    predict_image = results[0]

    # Get box with the highest percent (confidence)
    boxes = predict_image.boxes
    if len(boxes) < 1:
        logging.warning(f"Cannot find face in {source_img_path}. Skipping...") 
        return

    boxes_percents = [box.conf.item() for box in boxes]

    target_box = boxes[boxes_percents.index(max(boxes_percents))]
    target_box_info = target_box.xywh.tolist()

    # Just check box information
    logger.info(f"Target box information: {target_box_info}")
    # Getting box width and height, check it:
    source_h, source_w = source_image.shape[:2]
    logger.info(f"Source width: {source_w}, source height: {source_h}")

    target_box_w = target_box_info[0][2]
    target_box_h = target_box_info[0][3]
    is_full_frame = (target_box_w >= source_w - IMAGE_PADDING) or (target_box_h >= source_h - IMAGE_PADDING)

    # Create a canvas, and resize inner photo (source)
    if (target_box_info[0][2] > 180) and not is_full_frame:
        logger.warning("The photo width is greater than 180px. Trying to resize it...")

        if not Path("./tmp/").is_dir():
            os.mkdir("./tmp/")

        scale_factor = 0.6
        new_w = int(source_h * scale_factor)
        new_h = int(source_w * scale_factor)

        resized_inner_source = cv2.resize(source_image, (new_w, new_h), interpolation=cv2.INTER_AREA)
        white_canvas = np.full((source_h, source_w, 3), 255, dtype=np.uint8)
        x_offset = (source_w - new_w) // 2
        y_offset = (source_h - new_h) // 2

        white_canvas[y_offset:y_offset+new_h, x_offset:x_offset+new_w] = resized_inner_source

        tmp_path = f"./tmp/{save_filename}"

        cv2.imwrite(tmp_path, white_canvas)
            
        # Recursive
        make_crop(tmp_path, save_dir_path=save_dir_path, save_filename=save_filename, verbose=False, remove_tmp=False)
        return

    # Use padding, getting face
    img_h, img_w = source_image.shape[0], source_image.shape[1]

    x1, y1, x2, y2 = target_box.xyxy[0].tolist()

    x1_new = max(0, int(x1 - IMAGE_PADDING))
    y1_new = max(0, int(y1 - IMAGE_PADDING))
    x2_new = min(img_w, int(x2 + IMAGE_PADDING))
    y2_new = min(img_h, int(y2 + IMAGE_PADDING))

    image_face = source_image[y1_new:y2_new, x1_new:x2_new]
    resized_face = cv2.resize(image_face, (120, 120));

    # File save
    face_save_dir = save_dir_path.strip()
    face_filename = save_filename if (save_filename.endswith('.jpg')) else f"{save_filename}.jpg" 
    cv2.imwrite(f"{save_dir_path}/{save_filename}", resized_face)

    # Save predict_image to disk
    if save_detections:
        predict_image.save(f"{face_save_dir}/detections/detect_{face_filename}")

    if remove_tmp:
        remove_tmp_dir()


    # Turn on logger
    logger.disabled = False


def make_dir_crop(source_dir_path: str, save_dir_path: str, save_detections=True, verbose=True):
    if not os.path.isdir(source_dir_path):
        logger.warning(f"Cannot find {source_dir_path} or it is not a directory!")
        logger.warning(f"Please use the make_crop() function for files/photos.")
        return

    source_dir = Path(source_dir_path)

    names_list = [photo.name for photo in source_dir.iterdir()]

    for photo in source_dir.iterdir():
        make_crop(
            source_img_path=f"{source_dir_path}/{photo.name}",
            save_dir_path=save_dir_path,
            save_filename=f"{photo.name}_crop".replace(".jpg", "") + ".jpg",
            verbose=verbose,
            remove_tmp=False
        )

        # Remove tmp dir
        if photo.name == names_list[-1]:
            remove_tmp_dir()

def make_dir_watcher(watch_dir_path: str, save_dir_path: str, save_detections=True, verbose=True):
    if not os.path.isdir(watch_dir_path):
        logger.warning(f"Cannot find {watch_dir_path} or it is not a directory!")
        logger.warning(f"Please use the make_crop() function for files/photos.")
        return
    
    watch_dir = Path(watch_dir_path)

    event_handler = file_watcher.NewPhotoHandler(save_dir_path=save_dir_path, logger=logger)

    observer = Observer()
    observer.schedule(event_handler, path=watch_dir, recursive=True)
    observer.start()

    logger.info(f"[WATCHER] Watcher has started at {watch_dir}")

    try:
        while observer.is_alive():
            observer.join(1)

    except KeyboardInterrupt:
        pass

    finally:
        logger.info("[WATCHER] Watcher was stopped.")
        remove_tmp_dir()
        observer.stop()
        observer.join()

def remove_tmp_dir() -> None:
    if Path("./tmp/").exists():
        shutil.rmtree('./tmp/')

if __name__ == "__main__":
    log_level = logging.INFO
    logging.basicConfig(level=log_level, format='[%(asctime)s] %(levelname)s: %(message)s', datefmt='%I:%M:%S')

    make_crop(
        source_img_path="../static/pizda.jpg",
        save_dir_path="../save/",
        save_filename="pizda_crop.jpg",
        save_detections=True,
    )

    # make_dir_crop(source_dir_path="./test/", save_dir_path="./save/")

    # make_dir_watcher(watch_dir_path="./test/", save_dir_path="./save/")


# Сделать чтобы если лиц больше одного, то выбирало то, у которого больше процент. [x]
# Также, сделать чтобы могло принимать только одну фотку, а не целую папку. [x]
# Потом уже сделать метод для целой папки. [x]

# Сделать чтобы если width > 180, то он изменял размер холста изображения, на 30, и вновь вызывал make_crop. [x]
# Сделать чтобы он создавал папку tmp, где будет и храниться новое изображение с новым холстом, и в make_crop он отправляет именно [x]
# это изображние, рекурсивно, пока width не станет < 180 [x]

# Пофиксить: странные названия по типу 2cdea0bcaf1853ccb13cd6cfe5de0894 не сохраняются. [x]
# Они почему то не обрабатваются. [x]
# Ватчер их вообще не сохраняет [x]


#            x          y         w         h
# chibi: [364.1432, 335.7998, 373.7194, 306.3928]
# bread: [369.3522, 399.8462, 365.1479, 328.4302]


# alya1: [119.9251,  78.7224,  62.3473,  62.2945]
# alya2: [114.6406, 128.8411, 109.6239, 116.2071]
# alya3: [133.4062, 141.1047, 129.6302, 133.9397]
# alya4: [128.2774, 164.3281,  74.6416,  75.6569]
# alya5: [125.9256, 111.5175,  84.8933,  81.3283]
# alya6: [128.6105, 135.9117, 107.8001,  98.7769]
# alya7: [166.8384,  61.3762,  69.5930,  75.6840]
# alya8: [140.4814, 133.2510, 167.0629, 143.5779]


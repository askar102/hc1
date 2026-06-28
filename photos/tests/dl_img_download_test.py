import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import logging
import asyncio

from dl_source.downloader import PinterestDownloader

logger = logging.getLogger(__name__)

class TestImageHandle(unittest.TestCase):
    def test_img_handle(self):
            with PinterestDownloader(page_timeout=10, num_threads=5, min_resolution='0x0', size_compare_mode=None, logger=logger) as dl:
                img_list = dl.handle_image_links("https://pinterest.com/askar0704/alya/")
            
                with open('dl_img_download_test.log', 'w', encoding='utf-8') as f:
                    for img in img_list:
                        f.write(img + '\n')

                logger.info(f"Total images: {len(img_list)}")

                dl.download_by_image_links(links=img_list, download_folder='../static/')

if __name__ == "__main__":
    log_level = logging.INFO
    logging.basicConfig(level=log_level, format='[%(asctime)s] %(levelname)s: %(message)s', datefmt='%I:%M:%S')

    unittest.main()
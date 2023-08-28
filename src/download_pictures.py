import requests
from src.news import News
from robocorp import log
from RPA.Archive import Archive
import os
import shutil


class PictureDownloader:
    _pictures_folder = "output/pictures"
    _pictures_zip_output = "output/pictures.zip"

    @classmethod
    def download(cls, news: list[News]):
        os.mkdir(cls._pictures_folder)
        for n in news:
            try:
                if n.image_url:
                    cls._download_image(n.image_url, n.image_name)
            except Exception as e:
                log.exception(f"Download error: {e}, news: {n.to_dict()}")
        cls._zip_pictures()
        shutil.rmtree(cls._pictures_folder)

    @classmethod
    def _download_image(cls, image_url: str, image_name: str):
        response = requests.get(image_url)
        if response.ok:
            cls._save_image(response, image_name)
        else:
            log.warn(f"Could not download image, response: {response.text}")

    @classmethod
    def _save_image(cls, response, image_name):
        with open(f"{cls._pictures_folder}/{image_name}", "wb") as f:
            f.write(response.content)

    @classmethod
    def _zip_pictures(cls):
        archive = Archive()
        archive.archive_folder_with_zip(
            folder=cls._pictures_folder,
            archive_name=cls._pictures_zip_output,
            include="*.jpeg",
        )

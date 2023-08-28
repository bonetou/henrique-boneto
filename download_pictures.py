from src.download_pictures import PictureDownloader
from robocorp.tasks import task
from robocorp import workitems


@task
def download_news_pictures():
    payload = workitems.inputs.current.payload
    PictureDownloader.download(payload["news"])

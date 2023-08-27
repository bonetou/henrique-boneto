import requests
from news import News
from robocorp import log


class PictureDownloader:
    @classmethod
    def download(cls, news: list[News]):
        for n in news:
            try:
                if n.image_url:
                    response = requests.get(n.image_url)
                    if response.status_code == 200:
                        with open(f"output/{n.image_name}", "wb") as f:
                            f.write(response.content)
            except Exception as e:
                log.critical(f"Error downloading picture: {e}, news: {n}")

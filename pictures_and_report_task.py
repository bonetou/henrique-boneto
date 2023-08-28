from excel_report import ExcelReport
from src.download_pictures import PictureDownloader
from robocorp.tasks import task
from robocorp import workitems


@task
def download_pictures_and_generate_report():
    payload = workitems.inputs.current.payload
    PictureDownloader.download(payload["news"])
    ExcelReport.generate(payload["news"], payload["searchPhrase"])

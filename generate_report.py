from robocorp.tasks import task
from src.excel_report import ExcelReport
from robocorp import workitems


@task
def generate_excel_report():
    payload = workitems.inputs.current.payload
    ExcelReport.generate(payload["news"], payload["searchPhrase"])

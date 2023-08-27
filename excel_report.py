from news import News
from RPA.Excel.Files import Files


class ExcelReport:
    @classmethod
    def generate(cls, news: list[News], search_phrase: str):
        excel_lib = Files()
        content = [
            {
                **n.to_dict(),
                "search_phrase_count": n.count_search_phrase(search_phrase),
            }
            for n in news
        ]
        excel_lib.create_workbook("output/articles.xlsx")
        excel_lib.create_worksheet(name="articles",
                                   content=content, header=True)
        excel_lib.save_workbook()

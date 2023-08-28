import re
from RPA.Excel.Files import Files


class ExcelReport:
    @classmethod
    def generate(cls, all_news: list[dict], search_phrase: str):
        excel_lib = Files()
        content = [
            {
                "title": news["title"],
                "description": news["description"],
                "date": news["date"],
                "image_name": news["image_name"],
                "contains_amount_of_money": cls.has_any_amount_of_money(news),
                "search_phrase_count": cls._count(news, search_phrase),
            }
            for news in all_news
        ]
        excel_lib.create_workbook("output/articles.xlsx")
        excel_lib.create_worksheet(name="articles",
                                   content=content, header=True)
        excel_lib.save_workbook()

    @classmethod
    def _count(cls, news: dict, search_phrase: str) -> int:
        return (
            news["title"].lower().count(search_phrase.lower())
            + news["description"].lower().count(search_phrase.lower())
        )

    @classmethod
    def has_any_amount_of_money(cls, news: dict) -> bool:
        possible_money_patterns = [
            r'\$\d+(\.\d+)?',       # $11.1 | $111,111.11
            r'\d+\s*dollars',       # 11 dollars
            r'\d+\s*USD'            # 11 USD
        ]
        return any((
            re.search(pattern, news["title"])
            or re.search(pattern, news["description"])
            for pattern in possible_money_patterns
        ))

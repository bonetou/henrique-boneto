from src.excel_report import ExcelReport


def test_should_contain_when_possible_money_patterns_matches_in_title():
    patterns = [
        "$11.1",
        "$111,111.11",
        "11 dollars",
        "11 USD",
    ]
    for p in patterns:
        news = {
            "title": f"money money {p}",
            "description": "Sample news description.",
        }
        assert ExcelReport.has_any_amount_of_money(news)


def test_should_contain_when_possible_money_patterns_matches_in_description():
    patterns = [
        "$11.1",
        "$111,111.11",
        "11 dollars",
        "11 USD",
    ]
    for p in patterns:
        news = {
            "title": "No money",
            "description": f"A lot of money {p}",
        }
        assert ExcelReport.has_any_amount_of_money(news)

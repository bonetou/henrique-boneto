from news import News


def test_image_name_not_empty_when_there_is_url():
    news = News(
        title="Sample News Title",
        description="Sample news description.",
        raw_date="2 hours ago",
        image_url="http://example.com/image.jpg"
    )
    assert news.image_name.endswith(".jpeg")


def test_image_empty_when_there_is_no_url():
    news = News(
        title="Sample News Title",
        description="Sample news description.",
        raw_date="2 hours ago",
        image_url=""
    )
    assert not news.image_name


def test_should_contain_when_possible_money_patterns_matches_in_title():
    patterns = [
        "$11.1",
        "$111,111.11",
        "11 dollars",
        "11 USD",
    ]
    for p in patterns:
        news = News(
            title=f"money money {p}",
            description="Sample news description.",
            raw_date="2 hours ago",
            image_url=""
        )
        assert news.contains_any_amount_of_money is True


def test_to_dict():
    dict_news = News(
        title="Sample News Title",
        description="Sample news description.",
        raw_date="2 hours ago",
        image_url="http://example.com/image.jpg"
    ).to_dict()
    assert dict_news["title"] == "Sample News Title"
    assert dict_news["description"] == "Sample news description."
    assert dict_news["image_name"].endswith(".jpeg")
    assert dict_news["contains_amount_of_money"] is False

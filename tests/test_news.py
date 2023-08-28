from src.news import News


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

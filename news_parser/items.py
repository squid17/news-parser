import scrapy


class ArticleItem(scrapy.Item):
    title = scrapy.Field()
    body = scrapy.Field()
    external_links = scrapy.Field()
    categories = scrapy.Field()
    tags = scrapy.Field()
    pubdate = scrapy.Field()

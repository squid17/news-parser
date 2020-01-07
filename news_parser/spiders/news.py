import scrapy
import re
from scrapy.utils.project import get_project_settings
from datetime import datetime
from ..items import ArticleItem
from ..helpers import clean_html

settings = get_project_settings()


class NewsSpider(scrapy.Spider):
    name = "news"
    path = '/news-blog'
    articles = []

    def start_requests(self):
        yield scrapy.Request(url=settings.get('URL') + self.path, callback=self.parse)

    def parse(self, response):
        for post in response.xpath('//div[@class="news-content-box"]/h2/a/@href'):
            yield response.follow(post.get(), self.parse_article)

        next_page = response.xpath('//li[@class="next"]/a/@href').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def parse_article(self, response):
        article_parser = ArticleParser(response)
        yield ArticleItem(
            title=article_parser.get_title(),
            pubdate=article_parser.get_pubdate(),
            body=article_parser.get_body(),
            tags=article_parser.get_tags(),
            categories=article_parser.get_categories(),
            external_links=article_parser.get_external_links()
        )


class ArticleParser:
    """
    Parsing article page

    response: page data
    path: path of article
    """
    def __init__(self, response):
        self.response = response
        self.path = response.url.replace(settings.get('URL'), '')

    def get_title(self):
        return self.response.xpath('//h1[@class="inner-page-title"]/child::node()').get()

    def get_pubdate(self):
        results = re.findall(r"\w+ \d{1,2}, \d{4}", self.response.xpath(
            '//div[@class="views-field views-field-created"]/span[@class="field-content"]').get())
        if len(results):
            return datetime.strptime(results[0], '%B %d, %Y').strftime(settings.get('DATE_FORMAT'))
        return ''

    def get_tags(self):
        tags = []
        for tag_item in self.response.xpath(
                '//div[@class="views-field views-field-term-node-tid"]/span[@class="field-content"]/i/a/child::node()'):
            tags.append(tag_item.get())
        return tags

    def get_body(self):
        body_data = self.response.xpath('//article[@about="' + str(self.path) + '"]/div/div/div/div').get()
        return clean_html(body_data)

    def get_categories(self):
        categories = []
        for category in self.response.xpath('//ol[@class="breadcrumb"]/li/a/child::node()'):
            categories.append(category.get())
        return categories[1:len(categories)]

    def get_external_links(self):
        external_links = []
        for link in self.response.xpath('//article[@about="' + str(self.path) + '"]/div/div/div/div/.//a/@href'):
            link = link.get()
            if settings.get('URL') not in link and 'http' in link:
                external_links.append(link)
        return external_links

import psycopg2
from scrapy.utils.project import get_project_settings
from .helpers import list_to_string

settings = get_project_settings()


class NewsPipeline(object):
    def open_spider(self, spider):
        self.connection = psycopg2.connect(host=settings.get('DB_HOST'),
                                           user=settings.get('DB_USER'),
                                           password=settings.get('DB_PASSWORD'),
                                           dbname=settings.get('DB_NAME'))
        self.cur = self.connection.cursor()
        self.init_table()
        self.delete_all_rows()

    def init_table(self):
        """
        Table "article" initialization
        :return: None
        """
        self.cur.execute(
            'CREATE TABLE IF NOT EXISTS article (id serial PRIMARY KEY, article_body VARCHAR(20000)'
            ', categories VARCHAR(2000), title VARCHAR(255), pubdate VARCHAR(30), tags VARCHAR(1000),'
            'external_links VARCHAR(100000));')
        self.connection.commit()

    def delete_all_rows(self):
        """
        Delete articles from database
        :return: None
        """
        self.cur.execute("DELETE FROM article")
        self.connection.commit()

    def insert(self, article):
        """
        Insert article data in database
        :param article: data
        :return: None
        """
        self.cur.execute("INSERT INTO article (title, article_body, pubdate, tags, external_links, categories) "
                         "VALUES (%s, %s, %s, %s, %s, %s)", (article['title'], article['body'], article['pubdate'],
                                                             list_to_string(article['tags']),
                                                             list_to_string(article['external_links']),
                                                             list_to_string(article['categories'])))
        self.connection.commit()

    def process_item(self, item, spider):
        self.insert(item)
        return item

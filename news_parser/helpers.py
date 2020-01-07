import re


def clean_html(html):
    """
    Cleaning html from tags and iframe data
    :param html: html
    :return:
    """
    html = re.sub(re.compile('<.*?>'), '', html)
    return re.sub(re.compile('<iframe[^>]*>(.+?)</iframe>'), '', html)


def list_to_string(l):
    """
    Converting data from list to string split by comma
    :param l: list
    :return: string
    """
    return ', '.join(l)

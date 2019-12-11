from lxml import html
import requests
from pprint import pprint

header={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'}

def get_mail_news():
    main_link='https://mail.ru'
    response=requests.get(main_link, headers=header).text
    root=html.fromstring(response)
    news_data_mail=[]

    link=[]
    title_updated=[]
    authors=[]
    news_date=[]

    hrefs=root.xpath('//div[@class="news-item__inner"]/a/@href|//div[contains(@class,"news-item_main")]/a/@href')
    title=root.xpath('//div[@class="news-item__inner"]/a/text()|//h3[@class="news-item__title i-link-deco"]/text()')

    for href in hrefs:
        if href.startswith('https'):
            link.append(href)

    for t in title:
        if len(t)>10:
            t=t.replace('\xa0', ' ')
            title_updated.append(t)

    for l in link:
        response_news = requests.get(l, headers=header).text
        __root = html.fromstring(response_news)
        a=__root.xpath('//a[@class="link color_gray breadcrumbs__link"]//span[@class="link__text"]/text()')[0]
        datetime=__root.xpath('//@datetime')[0]
        datetime=(datetime[ : datetime.find("T")])
        authors.append(a)
        news_date.append(datetime)

    for i in range(len(link)):
        news_info = {}
        news_info['link'] = link[i]
        news_info['title']=title_updated[i]
        news_info['author']=authors[i]
        news_info['date']=news_date[i]
        news_data_mail.append(news_info)

    return news_data_mail

def get_lenta_news():
    main_link='https://lenta.ru'
    response=requests.get(main_link, headers=header).text
    root=html.fromstring(response)
    news_data_lenta = []

    link = []
    title = []

    partial_link=root.xpath('//div[@class="first-item"]/a/@href|//div[@class="span4"]/div[@class="item"]/a/@href')

    for p in partial_link:
        news_link=f'{main_link}{p}'
        link.append(news_link)

    news_titles=root.xpath('//div[@class="first-item"]/h2/a/text()|//div[@class="span4"]/div[@class="item"]/a/text()')

    for t in news_titles:
        t=t.replace('\xa0', ' ')
        title.append(t)

    date=root.xpath('//div[@class="first-item"]/h2/a/time/@title|//div[@class="span4"]/div[@class="item"]/a/time/@title')

    for i in range(len(link)):
        news_info = {}
        news_info['link'] = link[i]
        news_info['title']=title[i]
        news_info['author']='Lenta.ru'
        news_info['date']=date[i]
        news_data_lenta.append(news_info)

    return news_data_lenta


result=get_mail_news()+get_lenta_news()
pprint(result)

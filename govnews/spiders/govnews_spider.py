import scrapy
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector 
from govnews.items import GovnewsItem

class GovNewsSpider(CrawlSpider):
    name = "govnews"
    allowed_domains = ["gov.cn"]
    start_urls = [
        #"http://sousuo.gov.cn/column/31421"
        #"http://www.gov.cn/xinwen/yaowen.htm"
        "http://sousuo.gov.cn/column/31421/0.htm"
    ]
    rules={
        #Rule(LinkExtractor(allow='/tag/',restrict_xpaths="//div[@class='article']"),follow=True)
        #Rule(LinkExtractor(allow="\?start=\d+\&type=",restrict_xpaths="//div[@class='paginator']"),follow=True),
        #Rule(LinkExtractor(allow="/subject/\d+/$",restrict_xpaths="//ul[@class='subject-list']"),callback='parse_item')
        #Rule(LinkExtractor(allow="/column/31421/0.htm"), follow=True),
        Rule(LinkExtractor(allow="/column/31421/([\d]+).htm"), follow=True),
        Rule(LinkExtractor(allow="/",restrict_xpaths="//div[@class='news_box']"),callback='parse_item')
    }

        
    def parse_item(self, response):
        print("*"*50)
        print(response.url)

        item = GovnewsItem()
        #selector = Selector(None, response.body_as_unicode().replace('\r','').replace('\n',''), 'html') 
        if response.status == 200:
            try:
                selector = Selector(response)
                item['title'] = str(selector.xpath("//div[@class='article oneColumn pub_border']/h1/text()")[0].extract().strip().split('\n'))
                item['date'] = str(selector.xpath("//div[@class='pages-date']/text()")[0].extract().strip().split('\n'))
                item['body'] = str(selector.xpath("//div[@class='pages_content']/p/text()").extract())

                yield item
            except Exception as e:
                print("------------------------------------------error-----------------------------------------")
                print(response.url)
                print(e)
        else:
            print('*'*50)
        


        




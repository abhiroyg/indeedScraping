from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.exceptions import CloseSpider
from scrapy.http import Request
from scrapy import log
import random
import string

def random_string():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))

class DSJob(Spider):
    name = "ds"
    allowed_domains = ["indeed.com"]
    start_urls = [
        "http://www.indeed.com/jobs?as_and=&as_phr=data+scientist&as_any=&as_not=&as_ttl=&as_cmp=&jt=all&st=&salary=&radius=0&l=United+States&fromage=any&limit=10&sort=&psf=advsrch"
    ]

    def parse(self, response):
        self.log(response.url, level=log.DEBUG)
        sel = Selector(response)

        job_links = sel.xpath('//*[@class="jobtitle"]/a/@href').extract()
        self.log(job_links, level=log.DEBUG)
        page_texts = sel.xpath('//*[@class="pagination"]/a//text()').extract()[-1]
        self.log(page_texts, level=log.DEBUG)
        pages = sel.xpath('//*[@class="pagination"]/a/@href').extract()[-1]
        self.log(pages, level=log.DEBUG)
        page = sel.xpath('//*[@class="pagination"]/b/text()').extract()[0]
        self.log(page, level=log.DEBUG)
        titles = sel.xpath('//*[@class="jobtitle"]/a')
        self.log(titles, level=log.DEBUG)

        for i in xrange(10):
            title = ''.join(titles[i].xpath('.//text()').extract())
            self.log(title, level=log.DEBUG)
            url = 'http://www.indeed.com/viewjob?' + job_links[i][8:] + '&q=%22data+scientist%22&l=United+States&from=web'
            self.log(url, level=log.DEBUG)
            request = Request(url, callback=self.mediator,
                    meta={'page': page, 'title': title})
            yield request

        self.log(page_texts, level=log.DEBUG)
        self.log(pages, level=log.DEBUG)
        if "Next" in page_texts: 
            yield Request('http://www.indeed.com' + pages)

    def mediator(self, response):
        sel = Selector(response)
        redirect = sel.xpath('//*[@id="bvjl"]/a/@href')
        if len(redirect) > 0:
            yield Request('http://www.indeed.com' + redirect[0].extract(), callback=self.store_jobpost,
                    meta={'page': response.meta['page'], 'title': response.meta['title']})
        else:
            self.store_jobpost(response)

    def store_jobpost(self, response):
        self.log(response.url, level=log.DEBUG)
        sel = Selector(response)
        content = sel.xpath('/html').extract()[0].encode('utf-8')
        filename = response.meta['page'] + "_" + response.meta['title'] + "_" + random_string()  + ".html"
        filename = filename.replace("/", "")
        self.log('"' + filename + '"', level=log.DEBUG)
        with open('files/' + filename, 'wb') as f:
            f.write(content)

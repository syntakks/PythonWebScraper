import scrapy


class IetfSpider(scrapy.Spider):
    name = 'ietf'
    allowed_domains = ['pythonscraping.com']
    start_urls = ['http://pythonscraping.com/linkedin/ietf.html']

    def parse(self, response):
        #title = response.css('span.title::text').get()
        title = response.xpath('//span[@class="title"]/text()').get()
        descripiton = response.xpath('//meta[@name="DC.Description.Abstract"]/@content').get()
        date = response.xpath('//span[class="date"]/text()').get()
        author = response.xpath('//span[@class="author-name"]/text()').get()
        company = response.xpath('//span[@class="author-company"]/text()').get()
        rfc_count = response.xpath('//span[@class="rfc-no"]/text()').get()
        author_address = response.xpath('//span[@class="address"]/text()').get()
        author_phone = response.xpath('//span[@class="phone"]/text()').get()
        author_email = response.xpath('//span[@class="email"]/text()').get()
        return { 
            "title" : title,
            "description" : descripiton,
            "date" : date,
            "author" : author,
            "company" : company,
            "rfc_count" : rfc_count,
            "author_address" : author_address,
            "author_phone" : author_phone,
            "author_email" : author_email
            }

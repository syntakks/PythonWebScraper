# PythonWebScraper
LinkedIn Web Scraping tut.

Install Scrapy
Mac: pip3 install Scrapy

Windows: Install Anaconda, launch VS Code or cmd from their dashboard.
conda install -c conda-forge scrapy

Setup and Creates template files for Scrapy project:
scrapy startproject <your_projects_name_here>

Files:
scrapy.cfg: Scrapy configuration files.
items.py: Defines the objects or entities we are scraping. 
middlewares.py: Various Scrapy hooks.
pipelines.py: Defines functions that create and filter items.
settings.py: Project settings
spiders directory: Our spiders!

Create New Spider
scrapy genspider <spider_name_here> <scraping_destination_url_here>
example: scrapy genspider ietf pythonscraping.com
This will create a template spider.

In this example we will need to modify the start URL:
to 'http://pythonscraping.com/linkedin/ietf.html'

The parse function is how our spider interacts with the html returned from the response object.
This will need to return a dictionary with your scraped data.
example:
def parse(self, response):
    title = resposne.xpath('//span[@class="title"]/text()').get()
    return { "title" : title }
This looks for any text span with the class named "title" and returns it's text value.

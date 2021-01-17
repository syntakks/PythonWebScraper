# PythonWebScraper
LinkedIn Web Scraping tut.

Install Scrapy
Mac: pip3 install Scrapy... The easy route...

Windows: Install Anaconda, launch VS Code or cmd from their dashboard... ..The not so easy route...
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


Wiki:
Need to extend the CrawlSpider insted of scrapy.Spider in the class Definition.

settings.py: need to enable AutoThrottling to prevent wikipedia from denying our requests as they come in to quickly. 
AUTOTHROTTLE_ENABLED = True

Saving Article Data
Create the article item in items.py

You can save that data to an output csv file by using command flags. -o: output, -t: filetype, -s: settings.
There are issues with manually stopping the spider with ctrl+c as it uses multithreading while trying
to create an output file. It is better to set a limit of pages to crawl as below with the -s flag:
scrapy runspider wikipedia.py -o articles.csv -t csv -s CLOSESPIDER_PAGECOUNT=10
scrapy runspider wikipedia.py -o articles.json -t json -s CLOSESPIDER_PAGECOUNT=10

**Alternatively you can just specify these as global settings in the settings.py:
# Global Save Settings for our crawler
CLOSESPIDER_PAGECOUNT=10
FEED_URI='articles.json'
FEED_FORMAT='json'
Then our run command would be simple again:
scrapy runspider wikipedia.py

We can also specify spider specific settings in the wikipedia.py file:
These settings will override any global settings. Example:
custom_settings = {
    'FEED_URI': 'articles.xml',
    'FEED_FORMAT': 'xml'
}

# Validate and Clean articles in Pipeline
We can create and use pipelines to process our data as it comes in and drop items that are missing fields
as well as reformat the date string into a python datetime.
Each pipeline will be it's own class within the pipelines.py file.
Example:
class CheckItemPipeline:
    def process_item(self, article, spider):
        if not article['title'] or not article['url'] or not article['last_updated']:
            raise DropItem('Missing Article Data!, Dropping item...')
        return article

class CleanDatePipeline:
    def process_item(self, article, spider):
        article['last_updated'].replace('This page was last edited on', '').strip()
        article['last_updated'] = datetime.strptime(article['last_updated'], '%d %B %Y, at H%:%M')
        return article

We will need to tell scrapy that we would like to use these pipelines in the settings.py file:
(The number after the pipeline specifies the order in which the pipes should process the items, low to high)
# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'article_scraper.pipelines.CheckItemPipeline': 100,
    'article_scraper.pipelines.CleanDatePipeline': 200,
}
NOTE: If you intend on writing your item data to a database, the Pipeline is the place to do it.



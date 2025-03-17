# Scrapy settings for immuta_scraper project

BOT_NAME = "immuta_scraper"

SPIDER_MODULES = ["immuta_scraper.spiders"]
NEWSPIDER_MODULE = "immuta_scraper.spiders"

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure a delay for requests for the same website (default: 0)
DOWNLOAD_DELAY = 2

# Configure item pipelines
ITEM_PIPELINES = {
   # "immuta_scraper.pipelines.ImmutaScraperPipeline": 300,
}

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

# Add your user agent
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

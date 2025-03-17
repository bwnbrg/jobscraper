import scrapy
import json
from urllib.parse import urljoin
import re

class ImmutaJobsSpider(scrapy.Spider):
    name = "immuta_jobs"
    allowed_domains = ["immuta.com",
        "jobs.lever.co",
        "api.lever.co"]
    start_urls = ["https://api.lever.co/v0/postings/immuta"]

    def parse(self, response):
        self.logger.debug("Parsing response")
        postings = response.css("a").getall()
        for posting in postings:
            self.logger.debug(f"Processing posting: {posting}")
            pattern = r'<a\s+href="([^"]+)"[^>]*>(.*?)<\/a>'
            match = re.search(pattern, posting)
            if match:
                url = match.group(1)
                link_text = match.group(2)                
                self.logger.debug(f"Yielding url: {url}")
                yield scrapy.Request(
                    url=url,
                    callback=self.parse_job_details
                )

    def parse_job_details(self, response):
        """Parse the detailed job page"""
        
        self.logger.debug("Parsing job details")
        
        # Extract job details
        title = response.css(".posting-headline > h2::text").get()
        location = response.css("div .location::text").get()
        department = response.css("div .department::text").get()
                
        # Extract job description
        description = ' '.join(response.xpath("//div[@data-qa='job-description']//text()").getall()).strip()
        
        # Extract requirements
        requirements = ' '.join(response.css('ul.posting-requirements *::text').getall()).strip()
        
        # Yield the complete job information
        yield {
            'title': title,
            'location': location,
            'department': department,
            'url': response.url,
            'description': description,
            'requirements': requirements,
        }

# To run this spider:
# poetry run scrapy crawl immuta_jobs -o jobs.json
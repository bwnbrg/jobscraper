import scrapy
import json
from urllib.parse import urljoin


class ImmutaJobsSpider(scrapy.Spider):
    name = "immuta_jobs"
    allowed_domains = ["immuta.com"]
    start_urls = ["https://www.immuta.com/careers/"]

    def parse(self, response):
        """Parse the main careers page to find job listings"""
        # The job listings are loaded via JavaScript from a JSON file
        # We need to find and extract the data source
        
        # Looking at the page source, the jobs data is loaded from a script tag
        # Let's extract the script content that contains the job listings
        script_content = response.xpath('//script[contains(., "window.IMMUTA_OPEN_POSITIONS")]/text()').get()
        
        if script_content:
            # Extract the JSON data from the script
            try:
                # Find the start and end of the JSON data
                start_idx = script_content.find('window.IMMUTA_OPEN_POSITIONS = ') + len('window.IMMUTA_OPEN_POSITIONS = ')
                end_idx = script_content.find('};', start_idx) + 1
                
                # Extract and parse the JSON
                json_data = script_content[start_idx:end_idx]
                jobs_data = json.loads(json_data)
                
                # Process each job listing
                for department, jobs in jobs_data.items():
                    for job in jobs:
                        job_url = job.get('url')
                        if job_url:
                            # Add department info to the job data
                            job['department'] = department
                            
                            # Follow the link to the detailed job page
                            yield scrapy.Request(
                                url=job_url,
                                callback=self.parse_job_details,
                                meta={'job_data': job}
                            )
            except (json.JSONDecodeError, AttributeError) as e:
                self.logger.error(f"Error parsing job data: {e}")
        else:
            # Alternative approach: look for job links directly
            job_links = response.css('a.job-link::attr(href)').getall()
            for link in job_links:
                absolute_url = urljoin(response.url, link)
                yield scrapy.Request(url=absolute_url, callback=self.parse_job_details)

    def parse_job_details(self, response):
        """Parse the detailed job page"""
        # Get the job data from the previous request if available
        job_data = response.meta.get('job_data', {})
        
        # Extract job details
        title = response.css('h1.job-title::text').get() or job_data.get('title')
        location = response.css('div.job-location::text').get() or job_data.get('location')
        department = response.css('div.job-department::text').get() or job_data.get('department')
        
        # Extract job description
        description = ' '.join(response.css('div.job-description ::text').getall()).strip()
        
        # Extract requirements
        requirements = ' '.join(response.css('div.job-requirements ::text').getall()).strip()
        
        # Yield the complete job information
        yield {
            'title': title,
            'location': location,
            'department': department,
            'url': response.url,
            'description': description,
            'requirements': requirements,
            # Include any additional fields from job_data
            **{k: v for k, v in job_data.items() if k not in ['title', 'location', 'department', 'url']}
        }

# To run this spider:
# poetry run scrapy crawl immuta_jobs -o jobs.json
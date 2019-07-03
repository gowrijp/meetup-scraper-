from time import sleep
import scrapy
import selenium

from scrapy import Spider
from scrapy.selector import Selector
from scrapy.http import Request

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

class HomesSpider(Spider):
    name = 'homes'
    
    start_urls = ['https://www.meetup.com/find/events/?allMeetups=true&radius=Infinity&mcName=Where%3F']
    
    def parse(self, response):
        self.header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
        options = Options()
        options.add_argument("--disable-notifications")
        options.add_argument("--incognito")
        options.add_argument("--disable-extensions")
        options.add_argument(" --disable-gpu")
        options.add_argument(" --disable-infobars")
        options.add_argument(" -–disable-web-security")
        options.add_argument("--no-sandbox")
        caps = options.to_capabilities()
        self.driver = webdriver.Chrome('/usr/local/bin/chromedriver', desired_capabilities=caps)
        self.driver.get('https://www.meetup.com/find/events/?allMeetups=true&radius=Infinity&mcName=Where%3F')
        more_button = self.driver.find_element_by_xpath("//span[contains(@class,'button span-100')]")
        more_button.click()
        sleep(10.7)
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(7)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
            sleep(1.2)
        scrapy_selector = Selector(text = self.driver.page_source)
        link_selector = scrapy_selector.xpath("//div[contains(@class,'chunk')]/a[contains(@class,'resetLink big event wrapNice omnCamp omngj_sj7e omnrv_fe1 ')]//@href").extract() #name of an item can be changed by Airbnb
        self.logger.info('Theres a total of ' + str(len(link_selector)) + ' links.')
       
        
        q = 1
        for link in link_selector:
            self.logger.info('Home #' + str(q))
            self.driver.get(link)
            q = q+1
            sleep(10)
            link_to_home = link
            
            profile_scrapy_selector = Selector(text = self.driver.page_source)
            Heading = profile_scrapy_selector.xpath("//h1[contains(@class,'pageHead-headline text--pageTitle')]/text()").extract_first()
            Date = profile_scrapy_selector.xpath("//span[contains(@class,'eventTimeDisplay-startDate')]/span/text()").extract_first()
            Start_Time = profile_scrapy_selector.xpath("//span[contains(@class,'eventTimeDisplay-startDate-time')]/span/text()").extract_first()
            End_time = profile_scrapy_selector.xpath("//span[contains(@class,'eventTimeDisplay-endDate-partialTime')]/span/text()").extract_first()
            Recurrence = ''
            Recurrence = profile_scrapy_selector.xpath("//p[contains(@class,'eventTimeDisplay-recurrence text--caption')]/text()").extract_first()
            address_line1 = profile_scrapy_selector.xpath("//p[contains(@class,'wrap--singleLine--truncate')]/text()").extract_first()
            address_line2 = profile_scrapy_selector.xpath("//p[contains(@class,'venueDisplay-venue-address text--secondary text--small')]/text()").extract_first()
            How_to_reach = profile_scrapy_selector.xpath("//p[contains(@class,'text--caption text--wrapNice')]/text()").extract_first()
            Hosted_by = profile_scrapy_selector.xpath("//span[contains(@class,'text--secondary text--small')]/span[contains(@class,'link')]/text()").extract_first()
            Group_Name = profile_scrapy_selector.xpath("//span[contains(@class,'event-info-group--groupName link')]/text()").extract_first()
            Event_description = profile_scrapy_selector.xpath("//div[contains(@class,'event-description runningText')]/p/text()").extract()

            yield {
                            'link_to_home': link_to_home,
                            'Heading': Heading,
                            'Date': Date,
                            'Start_Time': Start_Time,
                            'End_time' : End_time,
                            'Recurrence' : Recurrence,
                            'address_line1': address_line1,
                            'address_line2': address_line2,
                            'How_to_reach' : How_to_reach,
                            'Hosted_by' : Hosted_by,
                            'Group_Name' : Group_Name,
                            'Event_description' : Event_description
                            }
        
    
        self.driver.close()

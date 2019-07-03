# meetup-scraper-
Scrapy project to scrape meetup.com using scrapy and selenium 

meetup.com is relying on a JS-heavy React framework, so Scrapy cannot get to the needed web elements and extract data from them. This is where Selenium comes in handy by virtually making a request to the server while also sending the headers that the server will accept without blocking your bot or distorting the data. Another thing that you notice, which calls for Selenium or alike— is the infamous infinite scroll.

In the *settings.py* file 1) DEFAULT_REQUEST_HEADERS, which are a part of any request your browser sends to the web server is added.


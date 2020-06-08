# -*- coding: utf-8 -*-
from time import sleep

from scrapy import Spider
from selenium import webdriver
from scrapy.selector import Selector
from scrapy.http import Request
from selenium.common.exceptions import NoSuchElementException


class BookselSpider(Spider):
    name = 'booksel'
    allowed_domains = ['books.toscrape.com']

    def start_requests(self):
        self.driver = webdriver.Chrome('D:\Haseeb\PIAIC\chromedriver.exe')
        self.driver.get('http://books.toscrape.com')

        sel = Selector(text=self.driver.page_source)
        books = sel.xpath('//h3/a/@href').extract()
        for book in books:
            url = 'http://books.toscrape.com/' + book
            yield Request(url, callback=self.parse_book)

        while True:
            try:
                next_page = self.driver.find_element_by_xpath('//a[text()="next"]')
                sleep(3)
                self.logger.info('Sleeping for 3 seconds.')
                next_page.click()

                sel = Selector(text=self.driver.page_source)
                books = sel.xpath('//h3/a/@href').extract()
                for book in books:
                    url = 'http://books.toscrape.com/catalogue/' + book
                    yield Request(url, callback=self.parse_book)

            except NoSuchElementException:
                self.logger.info('No more pages to load.')
                self.driver.quit()
                break

    def parse_book(self, response):
        book_title = response.xpath('//*[@id="content_inner"]/article/div[1]/div[2]/h1/text()').extract_first()
        book_price = response.xpath('//*[@id="content_inner"]/article/div[1]/div[2]/p[1]/text()').extract_first()
        book_description = response.xpath('//*[@id="content_inner"]/article/p/text()').extract_first()


        yield {
            'Book Title': book_title,
            'Book Price': book_price,
            'Book Describtion': book_description
        }



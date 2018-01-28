# -*- coding: utf-8 -*-
import scrapy

def cell_text(td):
    sel = 'div::text' if len(td.css('div')) else '::text'
    return td.css(sel).extract_first().strip()

class PriceListSpider(scrapy.Spider):
    name = 'price_list'
    allowed_domains = ['europegym.ru']
    start_urls = ['https://europegym.ru/centers/prices/1.html']

    def parse(self, response):
        for selector in response.css('.side_info:last-child a'):
            relative_link = selector.css('::attr(href)').extract_first()
            absolute_link = 'https://europegym.ru' + relative_link
#            print(absolute_link)
            yield scrapy.Request(url=absolute_link, callback=self.extract_prices)
        pass

    def extract_prices(self, response):
         rows = response.xpath('//h2[contains(text(), "Персональные тренировки")]/following-sibling::table[1]/tr')
         result = [[cell_text(td) for td in row.xpath('td')] for row in rows]
         print(result)



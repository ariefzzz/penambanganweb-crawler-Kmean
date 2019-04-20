# -*- coding: utf-8 -*-
import scrapy


from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ptaTrunojoyo.items import ItemTugasAkhir

class TugasakhirSpider(CrawlSpider):
    name = "TugasAkhir"
    allowed_domains = ['pta.trunojoyo.ac.id']
    start_urls = ['https://pta.trunojoyo.ac.id/welcome/index/4']


    rules = (
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//*[@id="end"]/ol/li[8]/a',)),
             callback="parse_item",
             follow=True),)


    def parse_item(self, response):
        print('Processing..' + response.url)

        item_links = response.css('a.gray.button::attr(href)').extract()
        # print(item_links)
        for a in item_links:
            print("membaca artikel .... "+a)
            yield scrapy.Request(a, callback=self.parse_detail_page)

    def parse_detail_page(self, response):
        judul = response.css('a.title::text').extract()[0].strip()
        penulis = response.xpath('//*[@id="content_journal"]/ul/li/div[2]/div[1]/span/text()').extract()[0]
        abstrak = response.xpath('//*[@id="content_journal"]/ul/li/div[4]/div[2]/p/text()').extract()[0]
        url = response.url

        penulis = penulis.replace('Penulis : ', '')

        # print((type(penulis)))
        # print("judul = " + judul)
        # print("penulis = " + penulis)
        # print("abstrak = " + abstrak)

        item = ItemTugasAkhir()
        item['judul'] = judul
        item['penulis'] = penulis
        item['abstrak'] = abstrak
        item['url'] = url
        yield item
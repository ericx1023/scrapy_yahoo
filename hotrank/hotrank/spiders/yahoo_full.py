# -*- coding: utf-8 -*-
import scrapy
# import _uniout

BASE_URL = 'https://tw.buy.yahoo.com'

class hotrankItem(scrapy.Item):
    text = scrapy.Field()
    price = scrapy.Field()

class YahooSpider(scrapy.Spider):
	name = "yahoo_miin"
	allowed_domains = ["tw.buy.yahoo.com"]
	start_urls = [
			"https://tw.buy.yahoo.com/help/helper.asp?p=sitemap&hpp=sitemap"
	]

	def parse(self, response):
		lis = response.xpath('//li[contains(concat(" ", @class, " "), " site-list ")]')
		anchors = lis.xpath('//li[contains(concat(" ", @class, " "), " site-list ")]/descendant::a')
		for li in lis:
			title = li.xpath('descendant-or-self::text()').extract()
			href = li.xpath('descendant-or-self::a/@href').extract()
			request = scrapy.Request(BASE_URL+href[0], callback=self.parse_hotrank, dont_filter=True)
			yield request

	def parse_hotrank(self, response):
		brand = response.xpath('//div[@id="cl-hotrank"]/descendant::div[@class="brand"]')
		uls = brand.xpath('ul[@class="pdset"]')
		for ul in uls:
			intro = ul.xpath('li[@class="intro"]')
			text = intro.xpath('div[@class="text"]/descendant::a/text()').extract()
			pd_price = intro.xpath('div[@class="pd-price"]')
			red_price = pd_price.xpath('span[@class="red-price"]')

			price = red_price.xpath('a/text()').extract()
			yield hotrankItem(
	        	price=price[0],
	        	text=text[0]
	        	)
# -*- coding: utf-8 -*-
import scrapy

class hotrankItem(scrapy.Item):
	title = scrapy.Field()
	href = scrapy.Field()

class YahooSpider(scrapy.Spider):
	name = "yahoo"
	allowed_domains = ["tw.buy.yahoo.com"]
	start_urls = [
			"https://tw.buy.yahoo.com/help/helper.asp?p=sitemap&hpp=sitemap"
	]

	def parse(self, response):
		
		lis = response.xpath('//li[contains(concat(" ", @class, " "), " site-list ")]')
		anchors = lis.xpath('//li[contains(concat(" ", @class, " "), " site-list ")]/descendant::a')
		for li in lis:
			title = li.xpath('descendant-or-self::text()')\
			.extract()
			href = li.xpath('descendant-or-self::a/@href')\
			.extract()
		        yield hotrankItem(
		        	title=title[0],
		        	href=href[0]
		        	)

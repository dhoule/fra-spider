# -*- coding: utf-8 -*-
import scrapy


class FiveringsarmorySpider(scrapy.Spider):
  name = 'fiveringsarmory'
  start_urls = ['http://fiveringsarmory.com/','https://fiveringsarmory.com/']
  handle_httpstatus_list = [404]

  def parse(self, response):
    yield { 
      'url': response.url,
      'title': response.css('title').get()
    }

    for a in response.css('a'):
      if "fiveringsarmory" in response.url:
        yield response.follow(a, callback=self.parse)
      else:
        yield response.follow(a, callback=self.parseLeaf)

  def parseLeaf(self, response):
    yield { 
      'url': response.url,
      'title': response.css('title').get()
    }
# -*- coding: utf-8 -*-
import scrapy


class FiveringsarmorySpider(scrapy.Spider):
  name = 'fiveringsarmory'
  start_urls = ['http://fiveringsarmory.com/']
  handle_httpstatus_list = [404]

  def parse(self, response):
    yield { 
      'title': response.css('title').get()
    }

    for a in response.css('a'):
      yield response.follow(a, callback=self.parse)

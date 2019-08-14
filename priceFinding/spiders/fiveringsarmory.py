# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.linkextractors import IGNORED_EXTENSIONS
import re # for Regex
import os # for environment variable

class FiveringsarmorySpider(scrapy.Spider):
  name = 'fiveringsarmory'
  allowed_domains = ['fiveringsarmory.com']
  # start_urls = ['http://fiveringsarmory.com/','https://fiveringsarmory.com/']
  start_urls = ['https://fiveringsarmory.com/login']
  handle_httpstatus_list = [404]
  rules = [
    Rule(LinkExtractor(deny=['\.pdf','\.jpg',]),follow=False)
  ]

  def parse(self, response):
    return scrapy.FormRequest.from_response(
      response, 
      formdata={'email': os.environ['FRAUSERNAME'], 'password': os.environ['FRAPASSWORD']},
      callback=self.after_login
    )

  def after_login(self, response):
    if "Error while logging in" in response.body:
      self.logger.error("Login failed!")
      return
    
    # This is to redirect to the front page after a successful login
    return scrapy.Request(url="https://fiveringsarmory.com/", callback=self.doTheThing)

  def doTheThing(self, response):
    url = response.url
    if (re.search("\.jpg",url) == None) and (re.search("\.pdf",url) == None):
      yield { 
        'url': url,
        'title': response.css('title').get()
      }

    for a in response.css('a'):
      # Used to filter the next call, because apparently, I can't get the Rule working
      temp = a.attrib['href']
      # Only follow "fiveringsarmory" links to actual websites
      if ("fiveringsarmory" in temp) and (re.search('\.jpg',temp) == None) and (re.search('\.pdf',temp) == None):
        yield response.follow(a, callback=self.doTheThing)



# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy_splash import SplashRequest
import re # for Regex
import os # for environment variable

# The point of this function is to build the `start_urls` array
def buildUrls():
  builtUrls = []

  # This is what the `search` URL looks like without the `Keywords` value
  body = "https://www.rsrgroup.com/search?Category=all&action=Search&Keywords="
  # body = "https://www.rsrgroup.com/product/"

  # Hard coding these for now
  referenceNums = ["MGHK229845S"]#["AISLR106-21", "ANGAAUDP09R16", "ARML15EAMFT", "ARMLDEF15", "ARMLDEF15F", "ARMLM153GN13",
    # "ARMLM15LTC16", "ARMLM15TAC16", "AUM130", "AUM150", "AUT1", "AUT1100D", "AUT150D", 
    # "AUT1B-14", "AUT1B50D", "AUT1C", "AUT5", "AUTM1C", "BCM650-111", "BCM750-133", 
    # "BCM750-140", "BCM750-790", "BCM750-790-BRZ", "BCM780-140", "BCM780-790", "BCMLRG-PISTOL", 
    # "BFM13305", "BFM13316", "BFM14354", "BM90216", "BM90325", "BM91046", "BM91047", "BM91048",
    # "BRO-SPEC15", "CARI2424-N", "CMMG30AF8C3", "CMMG48A7A84", "CMMG48A7AAA", "CMMG55AC72C", 
    # "CMMG76AFC3E", "CMMG76AFC41", "CMMG76AFCD7", "CZ45502100", "CZ45502105", "CZ45502106", 
    # "CZ45502107", "CZ45502110", "CZ45502111", "CZ45502114", "CZ45502140", "CZ45502170", 
    # "CZ51202260", "CZ52703019", "CZ52703072", "CZ75005001", "DD02-050-15027", 
    # "DD02-088-06027-011", "DD02-123-16029-047", "DD02-128-02081-047", "DD02-128-02241-047", 
    # "DD02-145-15175-047", "DD02-150-17029-047", "DD02-151-00257-047", "DD02-151-12033-047", 
    # "DD02-151-20026-047", "DD02-151-30032-047", "FN36318", "FN36320", "FN56460", "HENH004S", 
    # "LWICA2R5B16", "LWICA5R5B16", "LWICER5B14P", "MAR1895", "MAR70PSS", "MAR795", "MARXT-22", 
    # "NC22RB-UPPER-16-KIT", "NCNC15-223-16-BLK-XL", "NCNC15-223-18-BLK-XL", 
    # "NCNC15-300-16-BLK-XL", "NOS39648", "POF00856", "SPAA9611", "STY263463B", "STY263463E", 
    # "STY263463M", "STYSTG77SA", "WWR16A4T", "WWR16FTT-308", "WWR16M4FTT", "WWR16M4FTT-762", 
    # "WWR16M4FTT-CF1", "WWR16M4LHRFT", "WWR16M4LHT", "WWR16SFSDHHT-300", "WWR20FSSFTSKV", 
    # "DD02-154-19029-067", "CARI2253-X", "AT00201", "BRJ30TA18", "BRJ30TM18", "BRJ30TT18", 
    # "CASG1667-N", "CZ06085", "CZ06093", "FIMEVPR-12-03", "FN3088929124", "FN3088929145", 
    # "MK31010", "MK31017", "MK31023", "MK31044", "MK31046", "MK32200", "MK32202", "MK75445", 
    # "UTASPS1BB1", "UTASPS1BM1", "UTASPS1CM2", "UTASPS1FD1", "UTASPS1OD1", "UTASPS1TG1", 
    # "HKM700009-A5", "ARM51416FC", "ARM51485FC", "AU1911BKO", "AUTA5", "BABABU45ACPBLK", 
    # "BARII45410", "BATD357MAG", "BATD45410", "BATD45ACP", "BCM503-890", "BCM610-890", 
    # "BRJS92F300M", "BRU2S45B", "BRU2S60B", "CAHG3788-N", "CMMG76A29B8", "CMMG76AE87C", 
    # "CZ7591086", "CZ7591087", "CZ7591620", "CZ91351", "CZK01615", "FIMEREXZERO1S-01", 
    # "FN66694", "FN66719", "FN66720", "FN66770", "FN66772", "FN66822", "FN66852", "FN66960", 
    # "FN66962", "FN66964", "FN66965", "FN66966", "FN66968", "GL1750201", "GL1950201", 
    # "GL2250201", "GL2350201", "GL2650201", "GL2750201", "GL3350201", "GL3430101", 
    # "GL3530101", "GL3650201FGR", "GL4350201", "GLPF2050201", "GLPF2050203", "GLPF2150201", 
    # "GLPF2950201", "GLPF3050201", "GLPG1750201", "GLPG1750201MOS", "GLPG1750203", 
    # "GLPG1950201", "GLPG1950203", "GLPG2050201", "GLPG2150201", "GLPG2150203", "GLPG2250201", 
    # "GLPG2250203", "GLPG2350201", "GLPG2350203", "GLPG2650201", "GLPG2750201", "GLPG3050201", 
    # "GLPG3150201", "GLPG3150203", "GLPG3250203", "GLPG3350201", "GLPG3430101", "GLPG3430103", 
    # "GLPG3530101", "GLPG3530103", "GLPG4030101MOS", "GLPG4030103MOS", "GLPG4130101", 
    # "GLPG4130103", "GLPH3050201", "GLUG2350201", "GLUG3530101MOS", "GLUG4130101MOS", 
    # "GLUG4130103MOS", "GLUI4250201", "HK700009FDELE-A5", "HK700009FDELEL-A5", 
    # "HK700040LEL-A5", "HK704037-A5", "HK704203-A5", "HK704302-A5", "HK704303-A5", 
    # "HK709001TLE-A5", "HK709203-A5", "HK709302-A5", "HK709303-A5", "HK730903S-A5", 
    # "HKM709031-A5", "HKM730901-A5", "KRKV45-PFD20", "KRKV45-PSBBL20", "KRKV45-PSBFD20", 
    # "KRKV90-CBL20", "SG1911-45-MAXM", "SG1911-45-S-TGT-CA", "SG1911-45-SSS-CA", 
    # "SG1911CO-45-T-C3", "SG1911FCA-45-NMR", "SG1911FTCA-45-ESCPN", "SG1911R-45-BSS-CA", 
    # "SG1911R-45-ESCPN", "SG220R-45-BSS", "SG220R-45-EQ-CA", "SG225A-9-BSS-CL", 
    # "SG225A-9-BSS-CLW", "SG226R-9-LEGION", "SG226R-9-LEGION-SAO", "SG226R-9-SCPN-CA", 
    # "SG226R-9-XTM-BLKGRY-CA", "SG229R-9-BSS-CA", "SG229R-9-LEGION", "SG238-380-DES", 
    # "SG238-380-ESB", "SG238-380-HD-CA", "SG238-380-NMR", "SG238-380-SAS", 
    # "SG238-380-SPARTAN", "SG320C-40-BSS", "SG320C-9-FDE", "SG320F-40-BSS", 
    # "SG938-22-B-TGT-AMBI", "SG938-9-BG-AMBI", "SG938-9-BRG-AMBI", "SG938-9-BSS-AMBI", 
    # "SG938-9-NMR-AMBI", "SG938-9-SAS-AMBI", "SGE2022-40-B", "SGE2022-9-B", 
    # "SGE26R-357-LEGION", "SGE26R-40-BSS", "SGE26R-40-LEGION", "SGE26R-9-BSS", 
    # "SGE26R-9-LEGION", "SGE26R-9-LEGION-SAO", "SGE29R-40-BSS", "SGE29R-9-BSS", 
    # "SGE29R-9-LEGION", "SGM11-A1", "SGMK-25", "SGMK-25-CA", "SGSP2022-40-B-CA", 
    # "SGSP2022-9-B-CA", "SPXD9101", "SPXD9101HC", "SPXD9102", "SPXD9102HC", "SPXD9302", 
    # "SPXD9402", "SPXD9611", "SPXD9611HC", "SPXD9645", "SPXD9801", "SPXD9801HC", 
    # "SPXD9802", "SPXD9802HC", "SPXD9821", "SPXD9822", "SPXDG9101", "SPXDG9101HC", 
    # "SPXDG9801FDEHC", "SPXDG9801HC", "SPXDG9802HC", "SPXDG9821", "SPXDG9821HC", 
    # "SPXDG9845BHC", "SPXDGT9101FDEHC", "SPXDM9459BHCOSP", "SPXDS93340BE", "SPXDS93340SE", 
    # "SPXDS9339BE", "SPXDS9339DEE", "SPXDS9339SE", "SPXDS9339YE", "STY39-611-2H", 
    # "STY39-621-2K", "STY39-713-2H", "STY39-723-2K", "STY39-811-2", "STY39-821-2", 
    # "STY39-911-2H", "STY39-921-2K", "SW10034", "SW10035", "SW10036", "SW10048", "SW10086", 
    # "SW10099", "SW10100", "SW10109", "SW10141", "SW10147", "SW10174", "SW10176", "SW10177", 
    # "SW10201", "SW10214", "SW10265", "SW10266", "SW10267", "SW10270", "SW103061", 
    # "SW103072", "SW106303", "SW108390", "SW108411", "SW108483", "SW108485", "SW108490", 
    # "SW109106", "SW109107", "SW109108", "SW109158", "SW109200", "SW109201", "SW109203", 
    # "SW109204", "SW109250", "SW109253", "SW109254", "SW109306", "SW109307", "SW109308", 
    # "SW109381", "SW11531", "SW11631", "SW123400", "SW123402", "SW123403", "SW123900", 
    # "SW123902", "SW123903", "SW150339-A", "SW150477-A", "SW150481-A", "SW150717-A", 
    # "SW150718-A", "SW150784", "SW150786", "SW150923", "SW150972", "SW160578", "SW160584-A", 
    # "SW160936-A", "SW162411", "SW162414-A", "SW162506-A", "SW162634", "SW162802-A", 
    # "SW163052-A", "SW163062", "SW163071", "SW163072", "SW163073", "SW163210", "SW163460-A", 
    # "SW163465-A", "SW163500-A", "SW163501-A", "SW163504-A", "SW163565", "SW163603-A", 
    # "SW163606-A", "SW163636-A", "SW163638-A", "SW163690", "SW163811-A", "SW164192-A", 
    # "SW164194-A", "SW164198-A", "SW164222-A", "SW164224-A", "SW164300", "SW170133-A", 
    # "SW170135-A", "SW170137-A", "SW170161-A", "SW170181-A", "SW170210-A", "SW170262-A", 
    # "SW170296-A", "SW170299-A", "SW170316-A", "SW170320", "SW170341", "SW178011", 
    # "SW178014-A", "SW178020", "SW178035", "SW178036", "SW178038", "SW178055", "SW178060", 
    # "SW180020", "SW180021", "SW180022", "SW180050", "SW187020", "SW187021", "SW206300", 
    # "SW206304", "SW209300", "SW209301", "SW209304", "SW209330", "SW209331", "SW209921", 
    # "SW220070", "SW223400", "WA2795400", "WA2796066", "WA2796067", "WA2796082", "WA2807076", 
    # "SW10178", "MGHK229750S", "MGHK207314S", "MGHK207339S", "MGHK223515S", "MGHK229845S", 
    # "MGHK229970S", "MGPMAA922-A1", "MGSV90022", "MGTC55019828", "MPIMAG020B", "MPIMAG024B", 
    # "MPIMAG212BLK", "MPIMAG230BLK", "MPIMAG566BLK", "MGSW19923", "MGMPI576BLK", "MGWC47", 
    # "MGFMKM9C1M10", "MGMPI550BLK", "MGGL1915", "MGETSGLK-19", "HO34579", "KER1301BW", 
    # "KER1306BW", "KER1313BLK", "KER1319", "KER1557TI", "KER1600", "KER1920"]

  for ref in referenceNums:
    builtUrls.append(body + ref)

  return builtUrls


class FiveringsarmorySpider(scrapy.Spider):
  
  name = 'fiveringsarmory'
  allowed_domains = ['rsrgroup.com']
  start_urls = ['https://www.rsrgroup.com']
  handle_httpstatus_list = [404]
  rules = [
    Rule(LinkExtractor(deny=['\.pdf','\.jpg',]),follow=False)
  ]

  def parse(self, response):
    url = 'https://www.rsrgroup.com/api/membership/1.0/member/authenticate'
    headers = {'Content-Type': 'application/json'}
    return scrapy.Request(
      url=url, 
      method='POST',
      headers=headers,
      body=json.loads({'Login': os.environ['FRAUSERNAME'], 'Password': os.environ['FRAPASSWORD'], 'redirect': ''}),
      callback=self.after_login
    )

  def after_login(self, response):
    jsonresponse = json.loads(response.text)
    print(jsonresponse)
    if "Account # or password is incorrect." in response.body:
      self.logger.error("Login failed!")
      return
    print("logged in")
    # Now, spider need to do the thing
    for search in buildUrls():
      # yield scrapy.Request(url=search, callback=self.doTheThing)
      yield SplashRequest(
        url=search, 
        callback=self.doTheThing, 
        endpoint='render.html', 
        args={'wait':1.0}
      )

    return


  def doTheThing(self, response):

    h = response.css('h1[id="page-title"] span::text').get()
    # Results in
    # RSR Part #: AUT1
    # Which is what I want
    if h == None:
      return

    l = response.css('li[class="list-group-item small"]')
    msrp = None
    rmap = None
    for li in l:
      t = li.css("::text").get().strip()
      if "MSRP" in t:
        msrp = li.css("STRONG::text").get()
      if "MAP" in t:
        rmap = li.css("STRONG::text").get()
      # Results in:
      # MSRP:
      # $1,400.00
      # Retail MAP:
      # $1,299.00
    if rmap == None:
      yield { 'reference': h.split(':')[1].strip(), 'msrp': msrp }
    else:
      yield { 'reference': h.split(':')[1].strip(), 'msrp': msrp, 'map': rmap }



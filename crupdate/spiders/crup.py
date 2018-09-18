# -*- coding: utf-8 -*-
import scrapy
import time
import os
import tablib



list_of_skills=['skills', 'total', 'attack', 'defence', 'strength', 'hitpoints', 'ranged', 'prayer', 'magic', 
                'cooking', 'woodcutting', 'fletching', 'fishing', 'firemaking', 'crafting', 'smithing',
                'mining', 'herblore', 'agility', 'thieving', 'slayer', 'farming', 'runecrafting', 'hunter', 'construction']
xp = [0, 83, 174, 276, 388, 512, 650, 801, 969, 1154, 1358, 1584, 1833, 2107, 2411, 2746, 3115, 3523, 3973, 4470,
        5018, 5624, 6291, 7028, 7842, 8740, 9730, 10824, 12031, 13363, 14833, 16456, 18247, 20224, 22406, 24815,
        27473, 30408, 33648, 37224, 41171, 45529, 50339, 55649, 61512, 67983, 75127, 83014, 91721, 101333,
        111945,123660, 136594, 150872, 166636, 184040, 203254, 224466, 247886, 273742, 302288, 333804, 368599, 407015, 449428,
        496254, 547953, 605032, 668051, 737627, 814445, 899257, 992895, 1096278, 1210421, 1336443, 1475581, 1629200, 1798808, 1986068,
        2192818, 2421087, 2673114, 2951373, 3258594, 3597792, 3972294, 4385776, 4842295, 5346332, 5902831, 6517253, 7195629,
        7944614, 8771558, 9684577, 10692629, 11805606, 13034431]
dataset = tablib.Dataset()
dataset.append_col(list_of_skills, header='Skills')
class CrupSpider(scrapy.Spider):

    name = 'crup'
    start_urls = ['https://crystalmathlabs.com/tracker/api.php?type=virtualhiscores&groupid=13096&count=1000/']
    def parse(self, response):
     try:
        task=self.task
        print("This is the value of task: " + task)
     except:
        os.kill
     data = response.body.decode('utf-8')
     splitted = (data.splitlines())
     for i,name in enumerate(splitted):
         if ',' in name:
             pos = name.find(',')
             nam = name[:pos]
             splitted[i] = nam
     for name in splitted:
         if task == "u" or task == "update":
             up_url = "https://crystalmathlabs.com/tracker/api.php?type=update&player=" + name
             yield scrapy.Request(up_url, callback=self.parseup)
         elif task == "c" or task == "collect":
                 stats_url = "https://crystalmathlabs.com/tracker/api.php?type=stats&player=" + name
                 newRequest = scrapy.Request(stats_url, callback=self.parsestat)
                 newRequest.meta['name'] = name
                 yield newRequest
         time.sleep(1)

     if task == "c" or task == "collect":
         try:
            file=open("/home/squirrelapprentice/Programming/R/Stats.xls", 'wb+')
         except:
            os.kill
         file.write(dataset.xls)

    def parseup(self, response):
        pass
    
    def parsestat(self, response):
        name = response.meta.get('name')
        data = response.body.decode('utf-8')
        splitted = (data.splitlines())
        for i,stat in enumerate(splitted):
             if ',' in stat:
                 pos = stat.find(',')
                 st = stat[:pos]
                 splitted[i] = st
        splitted.remove(splitted[0])
        for i,sta in enumerate(splitted):
            distance = 100000000
            level = 1
            for j,x in enumerate(xp):
                if (int(sta) - x) < distance and (int(sta) - x) > 0:
                    distance = int(sta) - x
                    level = j + 1
                    splitted[i] = str(level)
        splitted.remove(splitted[0])
        total = 0
        for j, stat in enumerate(splitted):
            total = total +  int(splitted[j])
        splitted.insert(0,str(total))
        splitted.insert(0, name)
        dataset.append_col(splitted)

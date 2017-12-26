# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3

class GovnewsPipeline(object):
    def open_spider(self,spider):
        self.con = sqlite3.connect('govnews.sqlite')
        self.cu = self.con.cursor()


    def process_item(self, item, spider):
        print("spider_name:"+spider.name)

        #insert_sql = "insert into govnews (title,date,body) values('{}', ' {}', ' {}')".format(item['title'],item['date'],item['body'])
        #print(insert_sql)
        self.cu.execute("insert into govnews(title,date,body) values(?,?,?)",(item['title'], item['date'], item['body']))
        self.con.commit()
        return item

    def spider_close(self,spider):
        self.con.close()

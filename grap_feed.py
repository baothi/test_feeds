#!/usr/bin/python
import os.path
import sys, getopt
import feedparser
import sqlite3


db = sqlite3.connect('db.sqlite3')
cur = db.cursor()

def sql_insert(cur):

    url_text = sys.argv[1]
    url_text = url_text.replace(',',' ')
    url_text = url_text.split()

    for url in url_text:
        category_name = str((url.split('/'))[-1])
        feed = feedparser.parse(url) #Parsing XML data
        check_name = cur.execute("SELECT EXISTS(SELECT name FROM rss_category WHERE name=?)",([category_name]))
        check_name = (list(check_name.fetchone()))[0]
        print("=====================", check_name)
        # check_id = cur.execute("SELECT id FROM rss_category WHERE name=?",([category_name]))
        # check_id = list(cur.fetchone())
        # print("======================", check_id)
        # if str((list(check_name.fetchone()))[0]) == '1':
        #     cur.execute("insert into rss_category(name) values(?)",([category_name]))
        # else:
        #     print("du lieu da duoc tim tha")
    db.commit()
    db.close()

sql_insert(cur)
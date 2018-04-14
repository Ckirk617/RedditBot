#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 14:42:46 2018

@author: cmariekirk
"""

import psycopg2

conn = psycopg2.connect(dbname='redditbot', user='postgres')
cur = conn.cursor()
cur.execute("INSERT INTO new_posts (title,url) VALUES ('2' , 'doll');")
conn.commit()
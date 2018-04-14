#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 10 22:24:44 2018

@author: cmariekirk

We're going to try to make a reddit bot boys

"""

import praw
import config
import time
import psycopg2


reddit = praw.Reddit(username = config.username,
                password = config.password,
                client_id = config.client_id,
                client_secret = config.client_secret,
                user_agent = "naddy's comment reader test v0.1")

conn = psycopg2.connect(dbname='redditbot', user='postgres')
cur = conn.cursor()

"""Automated bot that checks reddit.com/r/new every ten seconds and
adds the title and url of each posts to a postgres database"""


def store_new_posts():
    counter = 1
    while True: 
        for submission in reddit.subreddit('all').new(limit=10):
            remove_char=submission.title.replace("'","")
            sql_command = "INSERT INTO new_posts (id,title,url) VALUES ('%d','%s','%s');" % (counter,remove_char,submission.url)
            cur.execute(sql_command)
            conn.commit()
            counter += 1
        print("sleeping for 30 seconds")
        time.sleep(30)
        


store_new_posts()

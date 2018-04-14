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

"""Function below will retrieve some basic information from a given subreddit
This function accesses the 'new' category but we can also access
hot,guilded,controversial,new,rising,top"""


def store_new_posts():
    counter = 1
    while True: 
        for submission in reddit.subreddit('all').new(limit=3):
            remove_char=submission.title.replace("'","")
            sql_command = "INSERT INTO new_posts (title,url) VALUES ('%s','%s');" % (remove_char,submission.url)
            print(sql_command)
            cur.execute(sql_command)
            conn.commit()
            counter += 1
    print("sleeping for 10 seconds")
    time.sleep(10)



store_new_posts()

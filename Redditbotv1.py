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
import datetime


reddit = praw.Reddit(username = config.username,
                password = config.password,
                client_id = config.client_id,
                client_secret = config.client_secret,
                user_agent = "DataMonger's bot")

conn = psycopg2.connect(dbname='redditbot', user='postgres')
cur = conn.cursor()




def store_new_posts():
    """Automated bot that checks reddit.com/r/all/new every ten seconds and
    adds the title and url of each posts to a postgres database"""
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

def find_coffee_posts():
    """Automated bot that checks reddit.com/r/all/new every ten seconds for posts whose
    title's contain the world 'coffee' and sends the date, title, and url
    of each post to a postgres database"""
    while True:
        for submission in reddit.subreddit('all').new(limit=10):
            x=submission.title.lower()
            if x.find('coffee') != -1:
                print("Found Coffee Post!")
                remove_char=submission.title.replace("'","")    
                sql_command = "INSERT INTO coffee_posts (date,title,url) VALUES ('%s','%s','%s');" % (datetime.datetime.now(),remove_char,submission.url)
                cur.execute(sql_command)
                conn.commit()
            else:
                print("No posts found")
        time.sleep(30)

def rcoffee_collection():
    while True:
        for submission in reddit.subreddit('coffee').new(limit=1):
            last_post = ''
            if submission.url != last_post:
                remove_char=submission.title.replace("'","")    
                sql_command = "INSERT INTO rcoffee_posts (date,title,url) VALUES ('%s','%s','%s');" % (datetime.datetime.now(),remove_char,submission.url)
                cur.execute(sql_command)
                conn.commit()
                last_post = submission.url
                print('adding post to database')
            else:
                print('Repeated Post. Sleeping for 3 seconds')
            time.sleep(3)


rcoffee_collection()

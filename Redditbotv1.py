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

def check_posts(subreddit_name,limit_to_check=10,sleep_time=30):
    """
    Function that takes:
        subreddit_name: a string containing the name of the desired subreddit to check
        category: a string containing the desired category of posts - valid
                  arguments are 'new','hot','top','controversial','rising','gilded'
        limit_to_check: an integer containing the desired number of posts to check
                        default at 10 posts
        sleep_time: an integer representing the number of seconds to wait before
                    loop repeats and checking occurs again. Default at 30 seconds.
    
    Prints the title names of the captured results
    """
    while True: 
        for submission in reddit.subreddit(subreddit_name).new(limit=limit_to_check):
            print(submission.title)
        print("sleeping for" + " " + str(sleep_time) + " " +  "seconds")
        time.sleep(sleep_time)



def store_new_posts():
    """Automated bot that checks reddit.com/r/all/new every ten seconds and
    adds the title and url of each posts to a postgres database called "new_posts" """
    while True: 
        for submission in reddit.subreddit('all').new(limit=10):
            title=str(submission.title.replace("'",""))
            sql_command = "INSERT INTO new_posts (title,url) VALUES (%s,%s);"
            cur.execute(sql_command,(title,submission.url))
            conn.commit()
        print("sleeping for 20 seconds")
        time.sleep(20)

def find_coffee_posts():
    """Automated bot that checks reddit.com/r/all/new every ten seconds for posts whose
    title's contain the world 'coffee' and sends the date, title, and url
    of each post to a postgres database"""
    while True:
        for submission in reddit.subreddit('all').new(limit=10):
            x=submission.title.lower()
            if x.find('coffee') != -1:
                print("Found Coffee Post!")
                title=str(submission.title.replace("'",""))    
                sql_command = "INSERT INTO coffee_posts (date,title,url) VALUES (%s,%s,%s);" 
                cur.execute(sql_command,(datetime.datetime.now(),title,submission.url))
                conn.commit()
            else:
                print("No posts found")
        time.sleep(30)

def rcoffee_collection():
    """Automated bot that scans r/coffee and adds submission title, score, and url to postgresql database"""
    while True:
        for submission in reddit.subreddit('coffee').hot(limit=30):
            title=str(submission.title.replace("'","")) 
            score=submission.score
            url=str(submission.url)
            sql_command = "INSERT INTO rcoffee_posts (title,score,url) VALUES (%s,%s,%s);"
            cur.execute(sql_command,(title,score,url))
            conn.commit()
            print('adding post ' + str(submission.title))
            time.sleep(2)


check_posts('all',50)

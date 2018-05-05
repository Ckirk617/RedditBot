#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 14:49:02 2018

@author: cmariekirk
"""

import psycopg2

class bot(object):
    def __init__(self):
        self.database_name = None #this will not work psycopg2 does not support using db name as parameter
    
    def __str__(self):
        return ""
    
    
    class Reddit_Bot(bot):
        
        def check_new_posts(subreddit_name,limit_to_check=10,sleep_time=30):
        """
        Function that takes:
            subreddit_name: a string containing the name of the desired subreddit to check
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
                
                
        def store_new_posts(subreddit_name,limit_to_check=10,sleep_time=30):
        """ 
        Automated bot that takes a string - subreddit_name - and 
            checks an integer - num_to_check - many posts then  
            adds the title and url of each post to the postgres database 
            specified when initializing the Reddit_Bot class
        """
          while True: 
                    for submission in reddit.subreddit(subreddit_name).new(limit=limit_to_check):
                        title=str(submission.title.replace("'",""))
                        sql_insert = "INSERT INTO %s (title,url) VALUES (%s,%s);"
                        cur.execute(sql_insert,(self.database_name,title,submission.url))
                        conn.commit()
                    print("sleeping for" + " " + str(10) + " " +  "seconds")
                    time.sleep(20)
        
        def keyword_search(keyword,subreddit_name,limit_to_check=10,sleep_time=30):
    """Automated bot that checks a specified subreddit's new posts every ten seconds f
    or posts whose title's contain the keyword and sends the date, title, and url
    of each post to a postgres database"""
    while True:
        for submission in reddit.subreddit(subreddit_name).new(limit=limit_to_check):
            x=submission.title.lower()
            if x.find(keyword) != -1:
                print("Found post containing keyword" + " " + keyword + " !")
                title=str(submission.title.replace("'",""))    
                sql_command = "INSERT INTO %s (date,title,url) VALUES (%s,%s,%s);" 
                cur.execute(sql_command,(self.database_name,datetime.datetime.now(),title,submission.url))
                conn.commit()
            else:
                print("No posts found, sleeping for" + " " + str(sleep_time) + " seconds...")
        time.sleep(sleep_time)
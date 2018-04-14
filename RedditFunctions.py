#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 10 22:24:44 2018

@author: cmariekirk

We're going to try to make a reddit bot boys

"""

import praw
import config
import pprint
import matplotlib.pyplot as plt
import time
import pyscopg2


reddit = praw.Reddit(username = config.username,
                password = config.password,
                client_id = config.client_id,
                client_secret = config.client_secret,
                user_agent = "naddy's comment reader test v0.1")

conn = pyscopg2.connect("dbname=redditbot user=cmariekirk")
cur = conn.cursor()


"""Code below counts how many times a specified word appears in the top ten
posts of a given subreddit"""
def title_word_count():
    counter = 0
    for submission in reddit.subreddit('coffee').hot(limit=10):
        prc = submission.title.lower()
        if "coffee" in prc:
            counter += 1
    print(counter)

"""Function below will retrieve some basic information from a given subreddit
This function accesses the 'new' category but we can also access
hot,guilded,controversial,new,rising,top"""
def retrieve_basic_subreddit_data(submission):
    for submission in reddit.subreddit(submission).new(limit=3):
        print(submission.title)
        #print(submission.score)
        print(submission.id)
        print(submission.url)


"""Function below calculates the average length of title submissions of the top 10
hot posts in a particular subreddit - here is r/coffee"""
def avg_title_len():
    titles = []
    for submission in reddit.subreddit('coffee').hot(limit=10):
        titles.append(len(submission.title))
    print(titles)
    avg = 0
    for i in titles:
        avg += i
    print("The average length of titles is: " + str(avg/len(titles)))

"""Another way to access a specific submission would be
   submission = reddit.submission(url='https://reddit.com/...)'
   or submission = reddit.submission(id='98jxae')
   then you could access its attribues such as
   submission.title or submission.score etc"""

"""Function below creates a dictionary containing the authors of
the top five reddit posts in a given subreddit and the score that
post received """
def top_authors_and_score():
    topauthors= {}
    for submission in reddit.subreddit('funny').top(limit=5):
        topauthors.update({submission.author.name:submission.score})
    print(topauthors)

"""Accessing Comments: The default submission.comments will display
the top comments sorted by best. If you want to iterate over all the
comments in a flattened list you can call the list method - see below:
    top_level_comments = list(submission.comments)
    all_comments = submission.comments.list()
    
You can also change the sort order by updating the value of comment_sort
on submission prior to accessing comments. See below:
    submission = reddit.submission('id=39zje0
    submission.commen_sort = 'new'
    top_level_comments = list(submission.comments)"""

"""The function below will display the contents of the top comments 
of a specified post"""
def get_comments():
    for submission in reddit.submission(id='8c7139').comments:
        print(submission.body)

"""The function below calculates the average length of the top 
comments for a specified post """
def avg_comm_len():
    commlen = []
    avg = 0
    for submission in reddit.submission(id='8c7139').comments:
        commlen.append(len(submission.body))
        avg += len(submission.body)
    print("The average length of a comment for post " + str(reddit.submission(id='8bg78e').title) +
            ' is ' + str(avg/len(commlen)) + " characters long.")

#Below will give a detailed list of attributes for the specified post
#submission = reddit.submission(id='8bg78e')
#print(submission.title)
#pprint.pprint(vars(submission))

"""Code below will create a scatter plot that takes the top 20 hottest posts in
a specified subreddit and plots the length of the title along the x-axis
and the score of the post along the y-axis as a scatterplot """
def title_len_vs_score():
    xvals=[]
    yvals=[]
    for submission in reddit.subreddit("politics").hot(limit=20):
        xvals.append(len(submission.title))
        yvals.append(submission.score)
    plt.scatter(xvals,yvals)
    plt.xlabel("Title length")
    plt.ylabel("Score")
    plt.show()
counter = 1



while True:
    retrieve_basic_subreddit_data('all')     
    print("sleeping for 10 seconds")
    time.sleep(10)



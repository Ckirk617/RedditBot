#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 18 17:35:47 2018

@author: cmariekirk
"""

import psycopg2
import matplotlib.pyplot as plt
import numpy as np

conn = psycopg2.connect(dbname='redditbot', user='postgres')
cur = conn.cursor()

cur.execute("SELECT title,score FROM rcoffee_posts ORDER BY score DESC;")
#retrieves posts from Postgres database ordered by score

result = cur.fetchall()
#This places result into a tuple containing (title,score)

def get_titles_string(result):
    """ 
    Function will take all the titles from the result variable (a tuple containing title,score)
    and combine them into a single string for further analysis
    """
    titles_combined = ''
    for i in result:
        titles_combined = titles_combined + i[0] + ' '
    return titles_combined

def word_stats(word):
    """ 
    Function looks for instances of a given string in the query results of 
    rcoffee_posts postgres database which has returned the title and score of posts in
    reddit.com/r/coffee and returns the number posts the word appeared in and the max
    and average karma score
    """
    contains_word = ()
    instances_word = 0
    for pair in result:
        if word in pair[0]:
            contains_word += pair
    word_score_list = []
    for scores in contains_word:
        if type(scores) == int:
            word_score_list.append(scores)
        else:
            instances_word += 1
    avg_word_score = np.mean(word_score_list)
    max_word_score = max(word_score_list)
    print('The word ' + word + ' appeared in ' + str(instances_word) + ' posts') 
    print('The word had an average karma score of ' + str(avg_word_score))
    print('The word had a maximum karma score of ' + str(max_word_score))
          


def count_words(text):
    """ 
    Count the number of times a word occurs in text (str) Return
    dictionary where keys are unique words and values are word counts.
    Skip punctuation
    """
    text = text.lower()
    skips = [".",",",";",":","'",'"',"!","?","_","(",")","-","[","]","/","$","&"]
    for ch in skips:
        text = text.replace(ch,"")
    word_counts = {}
    for word in text.split(" "):
        #known word
        if word in word_counts:
            word_counts[word] += 1
        #unknown word
        else:
            word_counts[word] = 1
    return word_counts




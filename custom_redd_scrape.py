# -*- coding: utf-8 -*-
"""
Created on Sat Oct 24 23:10:00 2020

@author: sydac
"""

import praw

#REMOVE PERSONAL INFO BEFORE POSTING TO GIT
my_id = "t4lLgeuNyiG52A"
secret = "O6Ktnu27Uvz724_tA8WeHVyZaDM"
agent_name = "Fake News Sharing Patterns"

#URL of API to which request URLS will be appended
r_api_url = "https://oauth.reddit.com"

#Login to Reddit with API and project information
reddit = praw.Reddit(
    client_id= my_id,
    client_secret= secret,
    user_agent= agent_name,
) 

my_subr = input("Please enter the name of a subreddit. Do NOT include r/ please.\n")
naughty_site = input("Please enter  a key word or domain of interest. For example, you may type \"washingtonpost.com/news\", \"wikipedia\", or \"tourist\".\n")

#access the most recent 500 posts of a subreddit my_subr
reddit_posts = reddit.subreddit(my_subr).top(limit=1000)

#Add the URLs of the reddit posts to a list, if that post has a score of at least 50
reddit_urls = []
reddit_scores = []
reddit_comments = []
for post in reddit_posts:
    if post.score >= 10:
        reddit_urls.append(post.url)
        reddit_scores.append(post.score)
        reddit_comments.append(post.num_comments)

reddit_data = [reddit_urls,reddit_scores,reddit_comments]

#A function to filter reddit self-posts from the list of post URLs. Returns True if someone posted a link to a naughty site and false otherwise.
naughty_count = 0
i = 0
found_guilty = False

naughty_reddit_urls = []
naughty_reddit_scores = []
naughty_reddit_comments = []
for reddit_url in reddit_urls:
    if naughty_site in reddit_url and not found_guilty:
        naughty_reddit_urls.append(reddit_urls[i])
        naughty_reddit_scores.append(reddit_scores[i])
        naughty_reddit_comments.append(reddit_comments[i])
        naughty_count += 1
        found_guilty = True
    i += 1
    found_guilty = False

naughty_reddit_posts = [naughty_reddit_urls,naughty_reddit_scores,naughty_reddit_comments]

post_count = len(reddit_urls)

for j in range(len(naughty_reddit_urls)):
    print("URL:", naughty_reddit_urls[j], "\nReddit Score:", naughty_reddit_scores[j], "\nNumber of comments:", naughty_reddit_scores[j], "\n")
if naughty_count == 0:
    print("There are", naughty_count, "posts out of", post_count, "posts which includes that phrase.")
elif naughty_count == 1:
    print("There is", naughty_count, "posts out of", post_count, "posts which includes that phrase. This post is described above.")
else:
    print("There are", naughty_count, "posts out of", post_count, "posts which include that phrase. These posts are described above.")
#an iterator created from the filtered list of URLs

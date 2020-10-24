import requests
import praw


#REMOVE PERSONAL INFO BEFORE POSTING TO GIT
my_id = "t4lLgeuNyiG52A"
secret = "O6Ktnu27Uvz724_tA8WeHVyZaDM"
agent_name = "Fake News Sharing Patterns"

#Login to Reddit with API and project information
reddit = praw.Reddit(
    client_id= my_id,
    client_secret= secret,
    user_agent= agent_name,
) 

hot_posts = reddit.subreddit('MachineLearning').hot(limit=10)
for post in hot_posts:
    print(post.title)
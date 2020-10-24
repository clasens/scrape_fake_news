import requests
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

all_urls = []
my_subr = "conservative"

#access the most recent 500 posts of a subreddit my_subr
my_posts = reddit.subreddit(my_subr).new(limit=500)

#Add the URLs of the reddit posts to a list, if that post has a score of at least 50
for post in my_posts:
    if post.score >= 50:
        all_urls.append(post.url)
    
#A function to filter reddit self-posts from the list of post URLs. Returns True for external URLs.
def self_post_filter(variable): 
    bad_words = ["i.redd.it", "https://www.reddit.com/r/"+my_subr+"/comments"]
    for word in bad_words:
        if (word in variable): 
            return False
        else: 
            return True
        
#an iterator created from the filtered list of URLs
filt_url = filter(self_post_filter, all_urls)

for site in filt_url:
    print(site)
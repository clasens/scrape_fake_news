# -*- coding: utf-8 -*-
"""
Created on Sat Oct 24 23:10:00 2020

@author: sydac
"""

import praw
import matplotlib.pyplot as plt
import pandas as pd


#REMOVE PERSONAL INFO BEFORE POSTING TO GIT
my_id = ""
secret = ""
agent_name = ""

#URL of API to which request URLS will be appended
r_api_url = "https://oauth.reddit.com"

#Login to Reddit with API and project information
reddit = praw.Reddit(
    client_id= my_id,
    client_secret= secret,
    user_agent= agent_name,
) 

try:
    run = False
    my_subr = input("Please enter the name of a subreddit. Do NOT include r/ please.\n")
    q = input("If you would like to search for fake news in your subreddit, type \"f\", and if you want to make your own search, type \"o\".\n")
    if q == 'f':
        naughty_site = None
        naughty_sites = open("fakesitelist.txt","r").read().split('\n')
        run = True
    elif q == 'o':
        naughty_site = input("Please enter a key word or domain of interest. For example, you may type \"washingtonpost.com/news\", \"wikipedia\", or \"tourist\".\n")
        run = True
    else:
        print('That is not a valid input')
    if run:
        ext = input("If you want to pull data from new posts, type \"n\", and if you want to pull data from top posts, type \"t\"\n")
        
        #access the most recent 500 posts of a subreddit my_subr
        run = False
        if ext == 'n':
            reddit_posts = reddit.subreddit(my_subr).new(limit=1000)
            run = True
        elif ext == 't':
            reddit_posts = reddit.subreddit(my_subr).top(limit=1000)
            run = True
        else:
            print('That is not a valid input')
        
        if run:
            #Add the URLs of the reddit posts to a list, if that post has a score of at least 50
            reddit_urls = []
            reddit_scores = []
            reddit_comments = []
            for post in reddit_posts:
                    if ("https://www.reddit.com/r/" not in post.url) and ("i.redd.it" not in post.url):
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
            if q = 'o':
                for reddit_url in reddit_urls:
                    if naughty_site in reddit_url and not found_guilty:
                        naughty_reddit_urls.append(reddit_urls[i])
                        naughty_reddit_scores.append(reddit_scores[i])
                        naughty_reddit_comments.append(reddit_comments[i])
                        naughty_count += 1
                        found_guilty = True
                    i += 1
                    found_guilty = False
            else:
                for reddit_url in reddit_urls:
                    for naughty_site in naughty_sites:
                        if naughty_site in reddit_url and not found_guilty:
                            naughty_reddit_urls.append(reddit_urls[i])
                            naughty_reddit_scores.append(reddit_scores[i])
                            naughty_reddit_comments.append(reddit_comments[i])
                            found_guilty = True
                            naughty_count += 1
                    i += 1
                    found_guilty = False
            
            post_count = len(reddit_urls)
            
            if q = 'o':
                for j in range(len(naughty_reddit_urls)):
                    print("\nURL:", naughty_reddit_urls[j], "\nReddit Score:", naughty_reddit_scores[j], "\nNumber of comments:", naughty_reddit_comments[j])
                if naughty_count == 0:
                    print("\nThere are", naughty_count, "posts out of", post_count, "posts linking to an external site which includes that phrase.")
                elif naughty_count == 1:
                    print("\nThere is", naughty_count, "posts out of", post_count, "posts linking to an external site which includes that phrase. This post is described above.")
                else:
                    print("\nThere are", naughty_count, "posts out of", post_count, "posts linking to an external site which include that phrase. These posts are described above.")
            else:
                for j in range(len(naughty_reddit_urls)):
                    print("\nURL:", naughty_reddit_urls[j], "\nReddit Score:", naughty_reddit_scores[j], "\nNumber of comments:", naughty_reddit_comments[j])
                if naughty_count == 0:
                    print("\nThere are", naughty_count, "posts out of", post_count, "posts linking to a naughty external site.")
                elif naughty_count == 1:
                    print("\nThere is", naughty_count, "posts out of", post_count, "posts linking to a naughty external site. This post is described above.")
                else:
                    print("\nThere are", naughty_count, "posts out of", post_count, "posts linking to a naughty external site. These posts are described above.")
                #an iterator created from the filtered list of URLs
            
            if naughty_count > 0:
                my_data = [naughty_count,post_count-naughty_count]
                my_labels = 'keyword hits','other URLs'
                plt.pie(my_data,labels=my_labels,autopct='%1.1f%%')
                plt.title('Reddit Links in Chosen Subreddit')
                plt.axis('equal')
                plt.show()
                
                score_hist_titl = "Scores of Reddit Posts Linking to URL containing \"" + naughty_site + "\""
                score_df = pd.DataFrame({score_hist_titl : naughty_reddit_scores})
                score_hist = score_df.plot.hist(bins=10)
                score_box = score_df.plot.box()
                
                comm_hist_titl = "Number of Comments on Reddit Posts Linking to URL containing \"" + naughty_site + "\""
                comm_df = pd.DataFrame({comm_hist_titl : naughty_reddit_comments})
                comm_hist = comm_df.plot.hist(bins=10)
                comm_box = pd.DataFrame({comm_hist_titl : naughty_reddit_comments}).plot.box()
                
                d = {"Reddit Score": naughty_reddit_scores, "Number of Reddit Comments": naughty_reddit_comments}
                df = pd.DataFrame(data=d)
                scatter = df.plot.scatter(x="Reddit Score",
                              y="Number of Reddit Comments")
                
        nrs = naughty_reddit_scores
        nrs.sort()
        table = []
        for score in nrs:
            i = naughty_reddit_scores.index(score)
            table.append([naughty_reddit_scores[i], naughty_reddit_comments[i], naughty_reddit_urls[i]])
                
        df_table = pd.DataFrame(table,
                  columns=["Reddit Score", "Number of Reddit Comments", "Posted URL"])
        
        nrc2 = naughty_reddit_comments
        nrc2.sort()
        table2 = []
        for comments in nrc2:
            i = naughty_reddit_comments.index(comments)
            table2.append([naughty_reddit_comments[i], naughty_reddit_scores[i], naughty_reddit_urls[i]])
            
        df_table2 = pd.DataFrame(table2,
                  columns=["Reddit Score", "Number of Reddit Comments", "Posted URL"])
        
        df_table.to_csv('reddit_ordered_score.csv', index=False)
        df_table2.to_csv('reddit_ordered_comments.csv', index=False)
            
except BaseException:
      print("That subreddit either does not exist or is locked.")

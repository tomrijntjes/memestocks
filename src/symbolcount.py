import glob
import os
from datetime import datetime



def nearest_hour(ts):
    return datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:00:00Z')

def parse(posts):
    # how am I going to look for 500 ticker symbols efficiently?
    for post in posts:
        total = 0
        for s in companies:
            c = post["contents"].count(s[1])
            post[s[0]]=c
            total+=c

        if total > 0:
            yield post

def count_company_mentions(subreddit):
    for timestamp in glob.iglob("data/{0}/**".format(subreddit), recursive=False):
        hour = (nearest_hour(int(timestamp.split("/")[2])))
        for post in glob.iglob("{0}/**.txt".format(timestamp), recursive=False):
            with open(post) as p:
                yield {
                    "subreddit":subreddit,
                    "timestamp":timestamp,
                    "hour":hour,
                    "filename":post,
                    "contents":p.read()
                }

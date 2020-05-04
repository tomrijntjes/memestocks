import glob
import os
from datetime import datetime



def nearest_hour(ts):
    return datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:00:00Z')


def parse_filename(p):
    filename = p.split("/")[-1].replace(".txt","")
    if "parentid" in filename:
        _,parentid,_ ,postid,_ , score = filename.split("_")
    else:
        parentid = None
        _,postid,_,score = filename.split("_")
    return parentid,postid,score

def parse_raw_posts(subreddit):
    for timestamp in glob.iglob("/data/{0}/**/*".format(subreddit), recursive=False):
        print(timestamp)
        hour = (nearest_hour(int(timestamp.split("/")[3])))
        for post in glob.iglob(timestamp, recursive=False):
            parentid,postid,score = parse_filename(post)
            with open(post) as p:
                yield {
                    "subreddit":subreddit,
                    "timestamp":timestamp.split("/")[3],
                    "hour":hour,
                    "parentid":parentid,
                    "postid":postid,
                    "score":score,
                    "contents":p.read()
                }

import glob
import os
from datetime import datetime
import csv


def scrub_company(c):
    # redditors often abbreviate company names
    postfixes = ["inc", "inc.","plc", "ltd.", "corp", "corp.","corporation","Incorporated", "class a", "class b","company", "& co","& co.","co","co."]
    resultwords  = [word for word in c.split() if word.lower() not in postfixes]
    return ' '.join(resultwords)

with open("dags/src/referencedata/SPY500.csv") as f:
    reader = csv.reader(f)
    companies = [(row[0],scrub_company(row[1])) for row in reader][1:]


def parse(post):
    """
    {'subreddit': 'investing', 'timestamp': '1587992169', 'hour': '2020-04-27 12:00:00Z', 'parentid': 'g8db7h', 'postid': 'fonlyf4', 'score': '1', 'contents': 'That makes sense. Thanks'}
    """
    for company in companies:
        if company[1] in post["contents"]:      # this can be improved upon 
            yield {
                "subreddit":post["subreddit"],
                "timestamp":post["timestamp"],
                "hour":post["hour"],
                "parentid":post["parentid"],
                "postid":post["postid"],
                "score":post["score"],
                "company":company[0]
            }

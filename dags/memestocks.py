import os
import time
import csv
from pathlib import Path
import praw
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator


from datetime import datetime

reddit = praw.Reddit(client_id=os.environ["CLIENT_ID"], client_secret=os.environ["CLIENT_SECRET"], user_agent=os.environ["USER_AGENT"])

def clean(s):
    return s.replace('\n', ' ').replace('\t', ' ').replace('\r',' ')

def scrape_subreddit(**kwargs):
    subreddit = kwargs["subreddit"]
    hot_posts = reddit.subreddit(subreddit).hot(limit=20)
    timestamp = int(time.time())
    basepath = "/data/{0}/{1}".format(subreddit,timestamp)
    Path(basepath).mkdir(parents=True, exist_ok=True)
    for post in hot_posts:
        print("[-] Collecting post and comments for post {0} with score {1}".format(post.id,post.score))
        with open("{0}/id_{1}_score_{2}.txt".format(basepath,post.id,post.score),"w+") as f:
            f.write(post.title)
            f.write("\n---------------\n")
            f.write(post.selftext)

        submission = reddit.submission(id=post.id)
        submission.comments.replace_more(limit=0)

        for comment in submission.comments.list():
            with open("{0}/parentid_{1}_id_{2}_score_{3}.txt".format(basepath,post.id,comment.id,comment.score),"w+") as f:
                f.write(comment.body)


with DAG('python_dag', description='Python DAG', schedule_interval='0 * * * *', start_date=datetime(2020, 1, 1), catchup=False) as dag:
        hot_investing_posts     = PythonOperator(task_id='hot_investing_posts', python_callable=scrape_subreddit, op_kwargs={"subreddit":"investing"})
        hot_stocks_posts        = PythonOperator(task_id='hot_stocks_posts', python_callable=scrape_subreddit, op_kwargs={"subreddit":"investing"})

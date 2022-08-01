# https://praw.readthedocs.io/en/latest/tutorials/refresh_token.html

from bs4 import BeautifulSoup

import praw
import re
import requests
import bs4


def authenticate():
    print('Authenticating...\n')
    reddit = praw.Reddit(
        'claire-bot',
        user_agent='reddit crawler by /u/idmontie'
    )
    print('Authenticated as {}\n'.format(reddit.user.me()))
    return reddit


def fetchdata(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')

    tag = soup.find('p')
    data = ''
    while True:
        if isinstance(tag, bs4.element.Tag):
            if (tag.name == 'h2'):
                break
            if (tag.name == 'h3'):
                tag = tag.nextSibling
            else:
                data = data + '\n' + tag.text
                tag = tag.nextSibling
        else:
            tag = tag.nextSibling

    return data


def run_explainbot(reddit):
    print("Getting 250 comments...\n")

    # TODO can we stream comments?
    # TODO how do we listen to multiple subreddits?
    for comment in reddit.subreddit('startups').comments(limit=250):
        match = re.findall(".*intercom.*", comment.body)
        if match:
            print("found a match")
            print(comment.body)

    print('Waiting 60 seconds...\n')

    # time.sleep(60)


def main():
    reddit = authenticate()
    # while True:
    run_explainbot(reddit)


if __name__ == '__main__':
    main()

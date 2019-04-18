# -*- coding: utf-8 -*-

import json, config
import pandas as pd
import csv
from requests_oauthlib import OAuth1Session


CK = config.CONSUMER_KEY
CS = config.CONSUMER_SECRET
AT = config.ACCESS_TOKEN
ATS = config.ACCESS_TOKEN_SECRET
twitter = OAuth1Session(CK, CS, AT, ATS)


def get_unique_list(seq):
    seen = []
    return [x for x in seq if x not in seen and not seen.append(x)]

def main():
    url = "https://api.twitter.com/1.1/search/tweets.json"
    CHECK_WORDS = 'アライさん'
    filename = "araisan.csv"

    params = {'q':'アライさん','count': 100, 'result_type' : 'recent'}
    r = twitter.get(url, params = params)

    results = []
    cnt = 0

    if r.status_code == 200:
        while True:
            search_timeline = json.loads(r.text)
            for tweet in search_timeline['statuses']:
                name = tweet['user']['name']
                screen_name = tweet['user']['screen_name']
                maxid = int(tweet["id"]) - 1
                cnt += 1

                if CHECK_WORDS in name:
                    print("{}:@{}".format(name,screen_name))
                    results.append(screen_name)

            if cnt >= 1000:
                break

            url = "https://api.twitter.com/1.1/search/tweets.json?count=100&lang=ja&q=" + CHECK_WORDS + "&max_id=" + str(maxid)
            r = twitter.get(url)

        results = list(set(results))
        f = open("./{}".format(filename),"w")
        for x in results:
            f.write(str(x) + "\n")
        f.close
    else:
        print("ERROR: %d" % r.status_code)


if __name__ == '__main__':
    print("Start")
    main()
    print("Done")
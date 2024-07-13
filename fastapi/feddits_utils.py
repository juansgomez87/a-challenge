from transformers import pipeline
from fastapi import HTTPException
from datetime import datetime
import requests

FEDDITS_URL = 'http://feddit:8080/api/v1/subfeddits/'
FEDDIT_URL = 'http://feddit:8080/api/v1/comments/'

nlp = pipeline(task='sentiment-analysis',
               model='cardiffnlp/twitter-roberta-base-sentiment-latest')


def get_sentiment(text):
    res = nlp(text)

    sent = res[0]['label']
    score = res[0]['score']

    # normalize scores from -1 to 1
    # -1 = completely negative
    # +1 = completely positive
    if sent == 'Negative':
        score *= -1
    return {'sentiment': sent, 'score': score}


def convert_timestamp_to_date(comments):
    for comment in comments:
        timestamp = comment['created_at']
        comment['created_at'] = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')  # noqa: E501
    return comments


def filter_comments_by_date(comments, start_date, end_date):
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')

    filtered_comments = [
        comment for comment in comments
        if start_date <= datetime.fromtimestamp(comment['created_at']) <= end_date  # noqa: E501
    ]
    
    return filtered_comments


def get_all_subfeddits():
    try:
        # fetch all fedits
        url = FEDDITS_URL + '?skip=0&limit=10'
        response = requests.get(url)
        response.raise_for_status()

    except requests.RequestException as e:
        # Handle any request errors
        raise HTTPException(status_code=500, detail='Error fetching data: {}'.format(str(e)))  # noqa: E501

    sub_dict = {_['id']: _['title'] for _ in response.json()['subfeddits']}

    return sub_dict


def get_comments_per_id(id, lim=25):
    try:
        # fetch all fedits
        url = FEDDIT_URL + '?subfeddit_id={}&skip=0&limit={}'.format(id, lim)
        response = requests.get(url)
        com = response.json()['comments']
        response.raise_for_status()

    except requests.RequestException as e:
        # Handle any request errors
        raise HTTPException(status_code=500, detail='Error fetching data: {}'.format(str(e)))  # noqa: E501

    return com

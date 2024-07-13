from fastapi import FastAPI, Query
from feddits_utils import get_sentiment, convert_timestamp_to_date, filter_comments_by_date, get_all_subfeddits, get_comments_per_id  # noqa: E501
from typing import Optional


app = FastAPI()


@app.get('/fetch-feddits')
async def fetch_all_feddits(name: Optional[str] = Query(None),
                            start_time: Optional[str] = Query(None),
                            end_time: Optional[str] = Query(None),
                            limit: Optional[str] = Query(None),
                            sort_score: Optional[str] = Query(None)):

    # get all subfeddits
    sub_dict = get_all_subfeddits()

    if not name:
        sub_id = 1
    else:
        # choose id depending on name
        sub_id = [k for k, v in sub_dict.items() if v == name][0]

    # get all comments
    comments = get_comments_per_id(sub_id, limit)

    # filter comments by user selection
    if start_time and end_time:
        comments = filter_comments_by_date(comments, start_time, end_time)

    # change timestamps
    comments = convert_timestamp_to_date(comments)

    # do sentiment analysis
    for com in comments:
        com.update(get_sentiment(com['text']))

    # sort comments by score or date
    if sort_score:
        comments = sorted(comments, key=lambda x: x['score'], reverse=True)
    else:
        comments = sorted(comments, key=lambda x: x['created_at'],
                          reverse=True)
    return comments


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get('/')
def welcome():
    return {'message': 'This is the Feddits sentiment analysis app'}


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)

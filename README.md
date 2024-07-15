# Challenge

The `docker-compose.yml` file provides access to `Subfeddit comment sentiment analysis` which completes the selected task. The task is achieved by using a recent method (2022) trained on Twitter [cardiffnlp/twitter-roberta-base-sentiment-latest](https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment-latest). 

The app is made up from a FastAPI app that looks for the data on the Feddit app and a Streamlit app that works as a frontend to the user. 

# How-to-run
1. Please make sure you have docker installed.
2. Make sure that the `Feddit` API is already running `docker compose -f feddits/docker-compose.yml up -d`.
3. To run the sentiment analysis, run `docker compose up --build`.
4. The app is now available at [http://0.0.0.0:8501](http://0.0.0.0:8501).

# Usage
Given the name of a subfeddit the application returns:
- A list of the most recent comments. Suppose a limit of 25 comments (this limit can be set on the slider).

For each comment:
+ **id**: unique identifier of the comment.
+ **username**: user who made/wrote the comment.
+ **text**: content of the comment in free text format.
+ **created_at**: timestamp in unix epoch time indicating when the comment was made/wrote.
+ **sentiment**: classification of the comment (positive, or negative).
+ **score**: the polarity score with values between -1 (negative) and 1 (positive).
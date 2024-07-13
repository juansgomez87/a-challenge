import streamlit as st
from datetime import datetime, timedelta
import requests

# Streamlit app title
st.title('Subfeddit comment sentiment analysis')

st.markdown('This app allows you to connect to a RESTful API \
    that selects a Subfeddit by title and performs a sentiment \
    analysis on a range of the comments. The comments will be \
    fetched from an API that connects to the Feddits API, use \
    a ML model to calculate the sentiment of the comments, and \
    retrieve the latest in the time range.')

st.markdown('**Comment**: Although the limit can be extended to \
    500 comments, have in mind that each of them is being processed\
    before returning all the comments.')

names = ['Dummy Topic 1', 'Dummy Topic 2', 'Dummy Topic 3']
selected_name = st.selectbox('Select Subfeddit', names)

start_date = st.date_input('Start date', value=datetime.now() - timedelta(days=30))
end_date = st.date_input('End date', value=datetime.now())

# Convert dates to string format for comparison
start_date_str = start_date.strftime('%Y-%m-%d %H:%M:%S')
end_date_str = end_date.strftime('%Y-%m-%d %H:%M:%S')

if start_date > end_date:
    st.error('Start date must be less than end date')

limit = st.slider('Select how many comments to retrieve', value=25, max_value=500)
sort_score = st.radio('Select to sort by polarity score:', ('False', 'True'), index=0)

sorter = sort_score == "True"

# Button to trigger the data fetch
if st.button('Get Comments'):
    if start_date and end_date:
        params = {
            'start_time': start_date,
            'end_time': end_date,
            'name': selected_name,
            'limit': limit,
            'sort_score': sorter
        }
        try:
            response = requests.get('http://fastapi:8000/fetch-feddits', params=params)
            response.raise_for_status()
            data = response.json()
            st.write(data)
        except requests.RequestException as e:
            st.error('Error fetching data: {}'.format(e))
    else:
        st.error('Please provide both start and end dates.')
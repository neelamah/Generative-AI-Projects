# frontented code
# it will use pipeline.py file to start app

import streamlit as st
from pipeline.pipeline import AnimeRecommendationPipeline
from dotenv import load_dotenv

st.set_page_config(page_title="Anime Recommnder",layout="wide")

load_dotenv()

#here we are using st.cache_resource to cache the pipeline object so that it is not reloaded every time the user interacts with the app. 
# This will improve the performance of the app by avoiding unnecessary reloading of the pipeline.
# AnimeRecommendationPipeline class ->  we are ccalling this class to create an instance of the pipeline which will be used to generate recommendations based on user query.
def init_pipeline():
    return AnimeRecommendationPipeline()

pipeline = init_pipeline()

st.title("Anime Recommender System")

query = st.text_input("Enter your anime prefernces eg. : light hearted anime with school settings")
if query:
    with st.spinner("Fetching recommendations for you....."):
        response = pipeline.recommend(query)
        st.markdown("### Recommendations")
        st.write(response)
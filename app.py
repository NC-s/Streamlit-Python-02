# Advantage for Streamlit

# Web frameworks like flask, you'll understand that unless you write
# specific code to implement some sort of cacheing mechanism

# Each update of the slider involves rerunning the entire script, meaning
# you'll be loading the 1.67 million rows of data over and over again, which
# can really put a dent in performance.

# But with stream lit, we can use a simple function decorator
# to intelligently cache the data

# Unless the input to the data or the data itself has been modified, the app
# will use the cache data over and over again to perform your computations

import sys
import subprocess
import streamlit as st
from streamlit.web import cli as stcli
from streamlit import runtime as st_runtime
from streamlit_jupyter import StreamlitPatcher, tqdm
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS

file_name = "app.py"
server_port = "8502"
DATA_URL = (
    "streamlit-demo-data/Tweets.csv"
)

StreamlitPatcher().jupyter()  # register streamlit with jupyter-compatible wrappers


def main():
    st.title("Sentiment Analysis of Tweets about US Airlines")
    st.sidebar.title("Sentiment Analysis of Tweets about US Airlines")
    st.markdown(
        "### This application is a Streamlit dashboard to analyze the sentiment of Tweets 🐦")
    st.sidebar.markdown(
        "### This application is a Streamlit dashboard to analyze the sentiment of Tweets 🐦")

    @st.cache_data(persist=True)
    def load_data():
        data = pd.read_csv(DATA_URL)
        data["tweet_created"] = pd.to_datetime(data["tweet_created"])
        return data

    data = load_data()
    # Keep the Unfiltered data for later use
    original_data = data

    # Section 1 - Show Random Wweet
    st.sidebar.subheader("Show random tweet")
    random_tweet = st.sidebar.radio(
        "Sentiment", ("positive", "neutral", "negative"))
    # Return a random tweet based on the sentiment selected from the radio button
    st.sidebar.markdown(data.query("airline_sentiment == @random_tweet")[[
        "text"]].sample(n=1).iat[0, 0])

    # Section 2 - Analyze the sentiment of Tweets
    st.sidebar.markdown("### Number of tweets by sentiment")
    # Create a new dataframe with the count of each sentiment
    select = st.sidebar.selectbox(
        "Visualization type", ["Histogram", "Pie chart"], key="1")

    sentiment_count = data["airline_sentiment"].value_counts()
    # Create a new dataframe with the count of each sentiment
    sentiment_count = pd.DataFrame(
        {"Sentiment": sentiment_count.index, "Tweets": sentiment_count.values})

    if not st.sidebar.checkbox("Hide", True):
        st.markdown("### Number of tweets by sentiment")
        if select == "Histogram":
            fig = px.bar(sentiment_count, x="Sentiment", y="Tweets",
                         color="Tweets", height=500)
            st.plotly_chart(fig)
        else:
            fig = px.pie(sentiment_count, values="Tweets", names="Sentiment")
            st.plotly_chart(fig)

    # This is the sentiment_count dataframe table
    st.subheader("Sentiment Count Table")
    st.write(sentiment_count)

    st.sidebar.subheader("When and where are users tweeting from?")
    # Hour to filter
    # Sidebar - Hours slider
    hour = st.sidebar.slider("Hour of day", 0, 23)
    # Sidebar - Hours number input
    # hour = st.sidebar.number_input("Hour of day", min_value=1, max_value=24)

    # Filter data based on the hour selected
    modified_data = data[data["tweet_created"].dt.hour == hour]
    if not st.sidebar.checkbox("Hide the Map based on the hour selected", True, key="2"):
        st.markdown("### Tweets locations based on the time of day")
        st.markdown("%i tweets between %i:00 and %i:00" %
                    (len(modified_data), hour, (hour+1) % 24))
        st.map(modified_data)
        # This is the sidebar checkbox to show the Filtered Data
        if st.sidebar.checkbox("Show Filtered Data", False):
            st.subheader("Filtered Data")
            st.write(modified_data)

    # Section 3 - Breakdown airline tweets by sentiment
    st.sidebar.subheader("Breakdown airline tweets by sentiment")
    choice = st.sidebar.multiselect(
        "Pick airlines", ("US Airways", "United", "American", "Southwest", "Delta", "Virgin America"), key="0")
    if len(choice) > 0:
        choice_data = data[data.airline.isin(choice)]
        fig_choice = px.histogram(choice_data, x="airline", y="airline_sentiment",
                                  histfunc="count", color="airline_sentiment",
                                  facet_col="airline_sentiment", labels={"airline_sentiment": "tweets"}, height=600, width=800)
        st.subheader("Breakdown airline tweets by sentiment")
        st.plotly_chart(fig_choice)

    # Section 4 - Word Cloud
    st.sidebar.subheader("Word Cloud")
    word_sentiment = st.sidebar.radio(
        "Display word cloud for what sentiment?", ("positive", "neutral", "negative"))

    if not st.sidebar.checkbox("Hide Word Cloud", True, key="3"):
        st.header(f"Word cloud for {word_sentiment} sentiment")
        df = data[data["airline_sentiment"] == word_sentiment]
        words = " ".join(df["text"])
        processed_words = " ".join(
            [word for word in words.split() if "http" not in word and not word.startswith("@") and word != "RT"])
        wordcloud = WordCloud(stopwords=STOPWORDS, background_color="white",
                              height=640, width=800).generate(processed_words)
        plt.imshow(wordcloud)
        plt.xticks([])
        plt.yticks([])

        # After December 1st, 2020, Streamlit will remove the ability to call st.pyplot() without any arguments.
        # It requires the use of Matplotlib's global figure object, which is not thread-safe.
        st.pyplot(plt)

    # Section 5 - Raw Data
    # This is the checkbox to show the original Raw Data
    if st.checkbox("Show Original Raw Data", False):
        st.subheader("Original Raw Data")
        st.write(original_data)

        # This is the checkbox to show the original Raw Data index & count
        original_data_count = len(original_data)
        original_data_index = original_data.columns
        if st.sidebar.checkbox("Show Original Raw Data Index & Count", False):
            st.write(original_data_index)
            st.write(original_data_count)


if __name__ == '__main__':
    if st_runtime.exists():
        main()
    else:
        subprocess.call(["streamlit", "run", file_name,
                        "--server.port", f"{server_port}"])

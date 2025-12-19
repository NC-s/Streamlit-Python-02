import pandas as pd

from app import (
    clean_tweets_for_wordcloud,
    filter_tweets_by_hour,
    get_airline_subset,
    get_sentiment_counts,
    load_data,
    sample_tweet_by_sentiment,
)


def test_load_data_has_required_columns():
    data = load_data()

    assert not data.empty
    assert "tweet_created" in data.columns
    assert pd.api.types.is_datetime64_any_dtype(data["tweet_created"])


def test_sentiment_counts_match_value_counts():
    data = load_data()
    counts = get_sentiment_counts(data)
    expected = data["airline_sentiment"].value_counts()
    reconstructed = counts.set_index("Sentiment")["Tweets"]

    assert reconstructed.to_dict() == expected.to_dict()


def test_filter_tweets_by_hour_respects_value():
    data = load_data()
    hour = 10
    filtered = filter_tweets_by_hour(data, hour)

    if not filtered.empty:
        assert filtered["tweet_created"].dt.hour.nunique() == 1
        assert filtered["tweet_created"].dt.hour.iloc[0] == hour
    else:
        # No tweets for the hour is acceptable; ensure empty frame has correct columns
        assert set(filtered.columns) == set(data.columns)


def test_sample_tweet_by_sentiment_returns_text():
    data = load_data()
    sentiment = data["airline_sentiment"].iloc[0]

    text = sample_tweet_by_sentiment(data, sentiment)

    assert isinstance(text, str)
    assert text.strip() != ""


def test_wordcloud_text_filters_links_and_mentions():
    data = load_data()
    processed = clean_tweets_for_wordcloud(data, "positive")

    assert "http" not in processed
    assert all(not token.startswith("@") for token in processed.split())


def test_airline_subset_filters_correctly():
    data = load_data()
    airline = "Delta"
    subset = get_airline_subset(data, [airline])

    if not subset.empty:
        assert set(subset["airline"].unique()) == {airline}

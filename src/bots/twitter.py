import tweepy
from datetime import datetime, timedelta, timezone
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger
from src.config import config

scheduler = BlockingScheduler()


class TweeterBot:

    def __init__(self, max_tweets: int = 1000):

        # Authenticate to Twitter
        auth = tweepy.OAuthHandler(config.twitter.api_key, config.twitter.api_secret)
        auth.set_access_token(config.twitter.access_token, config.twitter.access_secret)

        # Init the tweepy client
        self.api = tweepy.API(auth)

        # Init the bot parameters
        self.topics = config.twitter.topics
        self.interval = config.twitter.interval
        self.max_tweets = max_tweets

        # Set the interval of time to get tweets from
        self.last_tweet_time = datetime.now(timezone.utc) - timedelta(minutes=self.interval)

        self.initialize()

    def initialize(self):

        @scheduler.scheduled_job(IntervalTrigger(minutes=config.twitter.interval))
        def run():
            """
            Retrieve the tweets corresponding to the given topics, sanitize
            and filter them to get the most popular/interesting one, and
            retweet it on tweeter.
            """

            # Retrieve all tweets corresponding to the topics
            try:
                raw_tweets = []

                for term in self.topics:
                    raw_tweets += self.api.search(term, lang='en', result_type='recent', count=self.max_tweets)

            # Stop execution if an error occurred
            except Exception as error:
                print("Retrieving error: ", error)

            else:
                # Loop through all tweets and sanitize them
                found_tweets = []
                for tweet in self.__sanitize(raw_tweets):

                    # Remove the retweets
                    if ('retweeted_status' not in tweet

                            # Remove the tweets without link/image/video
                            and 'http' in tweet['text']

                            # Keep only the recent tweets
                            and self.__string_to_date(tweet['created_at']) > self.last_tweet_time):

                        # Save the filtered tweets
                        found_tweets.append(tweet)

                # Retweet the most liked/retweeted tweet
                self.__retweet(found_tweets)

    @staticmethod
    def __sanitize(tweets: list):
        """
        Generator that filter the tweets to get ride of all the
            unneeded information.
        :return: list
        """

        for tweet in tweets:
            yield tweet._json

    def __retweet(self, tweets: list):
        """
        Retweet a given tweet.

        :param tweets: The tweets to use to find the best tweet.
        :type: dict
        """

        # Retweet the tweet
        try:
            tweet = max(tweets, key=self.__math_tweet_popularity)
            self.api.retweet(tweet['id'])

        # Print the error if it occur
        except Exception as error:
            print("Retweeting error: ", error)

        else:
            # Reset the last time timestamp
            self.last_tweet_time = datetime.now(timezone.utc)
            print(f"[i] Tweet posted @ {self.last_tweet_time}")

    @staticmethod
    def __string_to_date(text: str) -> datetime:
        """
        Convert a Twitter datetime string to a Python datetime object.

        :param text: The datetime string to convert.
        :type text: str

        :return: A datetime object of the given text date.
        :rtype: datetime
        """
        return datetime.strptime(text, '%a %b %d %H:%M:%S %z %Y')

    @staticmethod
    def __math_tweet_popularity(tweet: dict) -> int:
        """
        Math the popularity of a tweet by summing and returning the
        amount and favorite and retweet.

        :param tweet: The tweet to math popularity.
        :type tweet: dict

        :return: The sum of favorites and retweets
        :rtype: int
        """
        return int(tweet['favorite_count']) + int(tweet['retweet_count'])

    @staticmethod
    def start():
        """Start all schedulers."""

        scheduler.start()

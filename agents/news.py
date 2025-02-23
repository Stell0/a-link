'''
Implements the Submodule class for the news agent.
Reads news_search_terms from params or environment variable NEWS_SEARCH_TERMS.
Searches for last week's news and trends on Twitter and logs them.
'''

import os
import json
import tweepy
from datetime import datetime, timedelta
from .Submodule import Submodule

class News(Submodule):
    """
    Submodule that searches for news and trends on Twitter for the specified search terms.
    """
    def run(self):
        """
        Search for last week's news on Twitter and log the results to stderr.
        """
        # Read search terms from params or environment variable
        search_terms = self.params.get('news_search_terms')
        if search_terms is None:
            env_terms = os.getenv('NEWS_SEARCH_TERMS')
            if env_terms:
                try:
                    search_terms = json.loads(env_terms)
                except json.JSONDecodeError:
                    self.logger.error("NEWS_SEARCH_TERMS is not a valid JSON array")
                    return
            else:
                self.logger.error("No search terms provided and NEWS_SEARCH_TERMS not set")
                return

        if not isinstance(search_terms, list):
            self.logger.error("search_terms should be a list")
            return

        # Set up Twitter API
        # Note: Ensure Twitter API credentials are set in the environment
        consumer_key = os.getenv('TWITTER_CONSUMER_KEY')
        consumer_secret = os.getenv('TWITTER_CONSUMER_SECRET')
        access_token = os.getenv('TWITTER_ACCESS_TOKEN')
        access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')

        if not all([consumer_key, consumer_secret, access_token, access_token_secret]):
            self.logger.error("Twitter API credentials are not fully set in environment variables")
            return

        try:
            auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_token, access_token_secret)
            api = tweepy.API(auth)
        except Exception as e:
            self.logger.error(f"Failed to authenticate with Twitter API: {str(e)}")
            return

        # Calculate the date for last week
        since_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')

        # Search for tweets containing the search terms
        for term in search_terms:
            try:
                # Note: Depending on your Twitter API tier, the exact method and parameters might vary
                tweets = api.search_tweets(q=term, lang='en', since_id=since_date, tweet_mode='extended')
                for tweet in tweets:
                    self.logger.info(f"Tweet by @{tweet.user.screen_name}: {tweet.full_text}")
            except Exception as e:
                self.logger.error(f"Failed to search tweets for '{term}': {str(e)}")
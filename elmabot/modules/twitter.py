import tweepy


class ElmaBotTwitter:
    def __init__(
            self,
            consumer_key, consumer_secret,
            access_token, access_token_secret):

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth)

    def get_my_tweets(self, count=5):
        tweets = tweepy.Cursor(
            self.api.user_timeline,
            count=count,
            trim_user=True,
            exclude_replies=True,
            contributor_details=False,
            include_entities=False,
            tweet_mode='extended',
            ).items(count)
        return tweets

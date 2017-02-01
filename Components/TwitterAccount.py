import tweepy
import datetime

from Components.Component import Component
from Components import auth

# start api session
CONSUMER_KEY = auth.CONSUMER_KEY
CONSUMER_SECRET = auth.CONSUMER_SECRET
ACCESS_KEY = auth.ACCESS_KEY
ACCESS_SECRET = auth.ACCESS_SECRET
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)


class TwitterAccount(Component):

    @property
    def state(self):
        return api.home_timeline(count=1)[0].text

    @state.setter
    def state(self, text):
        # TODO correct this
        current_time = datetime.datetime.now().time().strftime('%I:%M:%S %p')
        output = "The time of execution was " + str(current_time) + '   Message: ' + text
        api.update_status(output)

if __name__ == '__main__':
    twit = TwitterAccount('twit')
    twit.state = 'Working!'

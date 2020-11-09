# Functions to make the bot go vroom
import requests
#from bs4 import BeautifulSoup

def reply(botapi, username, tweetid, nextlyric):
  '''Reply to the user with the reply text given core Twython API handle, user screen name, and reply text.'''
  message = "@" + username + "\n" + nextlyric
  botapi.update_status(status=message, in_reply_to_status_id=tweetid) # create tweet


def mentions(data):
  '''Returns list of mentioned users and length of tagged section (to know when lyrics start).'''
  mentioned_users = []
  tagged_length = 0

  for entity in data["entities"]["user_mentions"]: # go through mentions
    mentioned_users.append(entity["screen_name"])  # add screen name
    tagged_length += len(entity["screen_name"])+2  # +2 for the @ symbol and space
  
  return mentioned_users, tagged_length


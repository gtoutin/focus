## MIT License
## 
## Copyright (c) 2020 G Toutin
## 
## Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to dealing the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
## 
## The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
## 
## THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


#import keep_alive
from twython import TwythonStreamer
from twython import Twython
import os
import particle
import sys
import requests
from notebook import whatsthatface

BOTNAME = "guitar_budgie"   # bot's twitter handle
OWNERNAME = "TheGuy13055669" # bot's owners' twitter handle

#in the following variables paste your own API keys
cons_key=os.environ.get('CONS_KEY')
cons_secret=os.environ.get('CONS_SECRET')
access_token=os.environ.get('ACCESS_TOKEN')
access_secret=os.environ.get('ACCESS_SECRET')

class MentionStream(TwythonStreamer):
    
  def on_success(self, data):
    print("Received tweet from",data["user"]["screen_name"])
    username = data["user"]["screen_name"]
    tweetid = data["id"]
    replytweetid = data["in_reply_to_status_id"]
    
    print(data)
    
    # create the bot's posting object
    botapi = Twython(cons_key, cons_secret, access_token, access_secret)
    
    # like tweet nevertheless
    botapi.create_favorite(id=tweetid) 

    # get list of certain people the user did name
    mentionedppl, tagged_length = particle.mentions(data) 
    
    # if the tweet mentions the bot and it's not the bot's tweet
    if (BOTNAME in mentionedppl and username!=BOTNAME):  
      print("It's a mention!")

      #save the information into photo
      photo = data['entities']['media'][0]['media_url'] #"image1.png" 
      photo = photo.split('/')
      photo = photo[-1]
      
      if( 'media' not in data['entities'].keys()):
          m= "tweet me an image:)"
          particle.reply(botapi, username, tweetid, m)
      else:
      # download the image with requests
        link = data['entities']['media'][0]['media_url']
        print(link)
        
        with open(photo, 'wb') as handle:
          response = requests.get(link, stream=True)
          if not response.ok:
            print(response, iter)

          for block in response.iter_content(1024):
            if not block:
              break

            # save the file
            handle.write(block) 

        #response = twitter.upload_media(media=photo)
    m = whatsthatface(photo)
    particle.reply(botapi, username, tweetid, m)

      #after tweeting the image we need to reset photo and delete the previous image
    os.remove(photo)
  
  def on_error(self, status_code, data):
    print(status_code)

# Keep the bot up!
#keep_alive.keep_alive()   

# Streaming bot
MetalDetector = MentionStream(cons_key, cons_secret, access_token, access_secret)
print("***** "*30)
print("You have entered AI MODE. COMMENCE TWEETING.")

while True:
  try:
      MetalDetector.statuses.filter(track=BOTNAME)
  except Exception:
    print("Error! Image probably has too many faces.")

      # this instance will dm me if the bot has an error
    errorbot = Twython(cons_key, cons_secret, access_token, access_secret)
    
    exc_type, value, traceback = sys.exc_info() # get error info

    errortext = str(exc_type) + "\n" + str(value) + "\n" + str(traceback)
    print(errortext)
      # get the owner's info
    ownerinfo = errorbot.lookup_user(screen_name=OWNERNAME)[0]

    dm_dict = {
        "event": {
          "type": "message_create",
          "message_create": {
            "target": {
              "recipient_id": ownerinfo["id"] # get the owner's id
            },
            "message_data": {
              "text": errortext
            }
          }
        }
      }

     # errorbot.send_direct_message(event=dm_dict['event'])

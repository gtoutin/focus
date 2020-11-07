## MIT License
## 
## Copyright (c) 2020 G Toutin
## 
## Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to dealing the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
## 
## The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
## 
## THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


import keep_alive
from twython import TwythonStreamer
from twython import Twython
import os
import particle
import sys

BOTNAME = "tmbgcompleter"   # bot's twitter handle
OWNERNAME = "guitar_budgie" # bot's owners' twitter handle

class MentionStream(TwythonStreamer):
    def on_success(self, data):
        print("Received tweet from",data["user"]["screen_name"])
        username = data["user"]["screen_name"]
        tweetid = data["id"]
        replytweetid = data["in_reply_to_status_id"]

        print(data)
        
        botapi = Twython(os.getenv("cons_key"), os.getenv("cons_secret"), os.getenv("access_token"), os.getenv("access_secret"))  # create the bot's posting object

        botapi.create_favorite(id=tweetid) # like tweet nevertheless

        # get list of certain people the user did name
        mentionedppl, tagged_length = particle.mentions(data) 
        
        # if the tweet mentions the bot and it's not the bot's tweet
        if (BOTNAME in mentionedppl and username!=BOTNAME):  
          print("It's a mention!")

          #Remove tags from text
          prevlyric = data["text"]
          prevlyric = prevlyric.replace("@","")
          for name in mentionedppl:
            prevlyric = prevlyric.replace(name, "")
          prevlyric = prevlyric.strip()

          if (len(data['text'])>tagged_length and prevlyric.lower()=='id'):  # if user just wants to id the song
            print("They want an ID!")

            find_id = True

            # Lyrics are in above tweet
            above_data = botapi.show_status(id=replytweetid)
            above_mentioned, above_length = particle.mentions(above_data)
          
            if (len(above_data["text"])<=above_length): # if the tweet above it doesn't have lyrics either
              emptymessage = "And right away I knew I made\nA mistake\nI left without my senses\nAnd I can't see anything\n\nOops! I don't see any lyrics."
              particle.reply(botapi, username, tweetid, emptymessage)

            else: # has lyrics above_data["text"]
              #Remove tags from text
              prevlyric = above_data["text"]
              prevlyric = prevlyric.replace("@","")
              for name in above_mentioned:
                prevlyric = prevlyric.replace(name, "")
              prevlyric = prevlyric.strip()
                            
              #Find the lyrics to the song
              lyrics, title = particle.search(prevlyric, find_id)

              if lyrics==None:  # Page not found error
                notfounderror = "Always busy, often broken.\n\nLyric not found.\nTry including more lyrics."
                particle.reply(botapi, username, tweetid, notfounderror)
                return  # end the function, there are no lyrics

              #Find the next lyrics in the page
              answerlyrics = particle.getnextlyric(prevlyric, lyrics, above_length)

              if find_id:
                id_message = 'That was from "' + title + '"'
                particle.reply(botapi, username, tweetid, id_message)
              elif answerlyrics==None:  # Lyric was the end of the song
                endofsongmessage = "Awesome! That was the end of the song."
                particle.reply(botapi, username, tweetid, endofsongmessage)
                return
              
              #Reply
              particle.reply(botapi, username, tweetid, answerlyrics)

          #----------------------------------------------
          elif (len(data["text"])>tagged_length): # tweet has lyrics
            print("They want the bot to answer!")
            
            # Add @tmbotg as a 100% correct source of lyrics
            if username=="tmbotg":
              prevlyric = '"' + prevlyric + '"' # Search for exact phrase

            #Find the lyrics to the song
            lyrics, title = particle.search(prevlyric, False)
            if lyrics==None:  # Page not found error
              notfounderror = "Always busy, often broken.\n\nLyric not found.\nTry including more lyrics."
              particle.reply(botapi, username, tweetid, notfounderror)
              return  # end the function, there are no lyrics

            #Find the next lyrics in the page
            answerlyrics = particle.getnextlyric(prevlyric, lyrics, tagged_length)
            
            if answerlyrics==None:  # Lyric was the end of the song
              endofsongmessage = "Awesome! That was the end of the song."
              print(endofsongmessage)
              particle.reply(botapi, username, tweetid, endofsongmessage)
              return
            else:
              print("Not the end of the song")
              #Reply
              particle.reply(botapi, username, tweetid, answerlyrics)

          #----------------------------------------------
          else: # if the tweet doesn't have lyrics, look above it
            print("They want to reply to a tweet above!")

            above_data = botapi.show_status(id=replytweetid)
            above_mentioned, above_length = particle.mentions(above_data)
          
            if (len(above_data["text"])<=above_length): # if the tweet above it doesn't have lyrics either
              emptymessage = "And right away I knew I made\nA mistake\nI left without my senses\nAnd I can't see anything\n\nOops! I don't see any lyrics."
              particle.reply(botapi, username, tweetid, emptymessage)

            else: # has lyrics above_data["text"]
              #Remove tags from text
              prevlyric = above_data["text"]
              prevlyric = prevlyric.replace("@","")
              for name in above_mentioned:
                prevlyric = prevlyric.replace(name, "")
              prevlyric = prevlyric.strip()
              
              #Find the lyrics to the song
              lyrics, title = particle.search(prevlyric)

              if lyrics==None:  # Page not found error
                notfounderror = "Always busy, often broken.\n\nLyric not found.\nTry including more lyrics."
                particle.reply(botapi, username, tweetid, notfounderror)
                return  # end the function, there are no lyrics

              #Find the next lyrics in the page
              answerlyrics = particle.getnextlyric(prevlyric, lyrics, above_length)

              if answerlyrics==None:  # Lyric was the end of the song
                endofsongmessage = "Awesome! That was the end of the song."
                particle.reply(botapi, username, tweetid, endofsongmessage)
                return
              
              #Reply
              particle.reply(botapi, username, tweetid, answerlyrics)
        

    def on_error(self, status_code, data):
        print(status_code)

        # Want to stop trying to get data because of the error?
        # Uncomment the next line!
        # self.disconnect()
    

keep_alive.keep_alive()   # Keep the bot up!

# My metal detector is with me all of the time
MetalDetector = MentionStream(os.getenv("cons_key"), os.getenv("cons_secret"), os.getenv("access_token"), os.getenv("access_secret"))

while True:
  try:
    MetalDetector.statuses.filter(track=BOTNAME)
  except Exception:
    # this instance will dm me if the bot has an error
    errorbot = Twython(os.getenv("cons_key"), os.getenv("cons_secret"), os.getenv("access_token"), os.getenv("access_secret"))

    exc_type, value, traceback = sys.exc_info() # get error info

    errortext = str(exc_type) + "\n" + str(value) + "\n" + str(traceback)
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

    errorbot.send_direct_message(event=dm_dict['event'])
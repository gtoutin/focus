# Functions to make the bot go vroom
import requests
from bs4 import BeautifulSoup

def reply(botapi, username, tweetid, nextlyric):
  '''Reply to the user with the reply text given core Twython API handle, user screen name, and reply text.'''
  message = "@" + username + "\n" + nextlyric
  botapi.update_status(status=message, in_reply_to_status_id=tweetid) # create tweet


def getnextlyric(text1, text2, tagged_length):
  '''Find the lyric after the query string in the lyrics string.
  Required query string, full lyrics string, and tagged_length int from mentions() denoting how many characters long the tagged section is.'''

  best_i = 0  # keeps track of where the earliest most similar text is
  best_similarity = 0

  for i in range(0, len(text2)-len(text1)):
    excerpt = text2[i:len(text1)+i]
    similar = similarity(text1, excerpt)

    if similar > best_similarity:
      best_i = i
      best_similarity = similar
  
  # Now get the next lyrics
  # beginning index is next new line
  begin_i = best_i + len(text1) # last character of text1
  rest_of_song = text2[begin_i:-1]  # get from the last character of input to the end of the song
  begin_i = rest_of_song.find("\n")+1 # +1 to not get the newline
  if begin_i==len(rest_of_song)-1 or len(rest_of_song) == 0:  # If lyrics were the last in song
    return None
  rest_of_song = rest_of_song[begin_i:-1]

  # Now get appropriate length of next lyrics
  tw_len = 280-tagged_length  # max tweet length
  newlines = findall(rest_of_song, "\n") # beep beep, detected newlines
  # Find the newline in the list that is less than tweet length or 3 lines long
  location = 0
  try:
    for i in newlines:
      if i==newlines[2] and i <= tw_len:  # Only want 3 lines
        location = i
        break
      elif i <= tw_len:  # Haven't exceeded tweet length, save and go on
        location = i
      else:
        location = tw_len-4 # Line is too long, cut it
        return rest_of_song[0:location] + "..." # add ellipsis
  except:
    location = newlines[-1] # Less than 3 lines left in song, take the rest

  next_lyrics = rest_of_song[0:location]

  return next_lyrics
 
def similarity(text1, text2):
  '''
  Given 2 texts of identical length, will output a percent similarity as a float between 0 and 1.
  Similarity is calculated by counting the frequency of letters among both texts, comparing the frequencies, and converting it to a percentage.
  '''

  alphabet = "abcdefghijklmnopqrstuvwxyz,.?'\":;()!1234567890\n "
  letter_dict1 = {}
  letter_dict2 = {}

  for letter in alphabet: # Letters are the keys, values are frequency
    letter_dict1.setdefault(letter,0) # Start every letter with 0 frequency
    letter_dict2.setdefault(letter,0)

  # Get frequencies for text1
  for letter in text1.lower(): 
    if letter in letter_dict1: 
        letter_dict1[letter] += 1
    else: 
        letter_dict1[letter] = 1

  # Get frequencies for text2
  for letter in text2.lower(): 
    if letter in letter_dict2: 
        letter_dict2[letter] += 1
    else: 
        letter_dict2[letter] = 1
  
  # Compare the 2 dictionaries to get the raw similarity
  # Start at 100% similar and take away points for differences.

  denominator = sum(letter_dict1.values()) # Both dicts have the same frequency sum. This is necessary to compute percentage.
  rawsimilarity = denominator # keeps track of how many letters are in common

  # Compare the frequencies of the contents of both dicts.
  for letter in letter_dict1:
    rawsimilarity -= abs(letter_dict1[letter]-letter_dict2[letter])
  
  return float(rawsimilarity / denominator)


def findall(s, ch):
  '''Helper function that finds all occurences of a character in a string and returns it as a list.
  Thanks to Lev Levitsky on Stack Overflow.'''
  return [i for i, ltr in enumerate(s) if ltr == ch]

def mentions(data):
  '''Returns list of mentioned users and length of tagged section (to know when lyrics start).'''
  mentioned_users = []
  tagged_length = 0

  for entity in data["entities"]["user_mentions"]: # go through mentions
    mentioned_users.append(entity["screen_name"])  # add screen name
    tagged_length += len(entity["screen_name"])+2  # +2 for the @ symbol and space
  
  return mentioned_users, tagged_length

def search(query, id_mode=False):
  '''Grab all the lyrics of the song from tmbw.net.'''
  searchurl = 'http://tmbw.net/wiki/index.php?title=Special%3ASearch&profile=advanced&fulltext=Search&ns100=1&profile=advanced&search=' + query
  data = requests.get(searchurl)  # get page data
  soup = BeautifulSoup(data.text,features="html.parser")  # parse page data
  element = soup.find("div", class_="mw-search-result-heading") # div with the link
  try:
    link = element.find("a").get('href')  # get the link
    title = element.find("a").get("title") # get page title
  except:
    print("Page not found")   # return None if no results were found
    return None, None

  data = requests.get("http://tmbw.net" + link)
  soup = BeautifulSoup(data.text,features="html.parser")
  element = soup.find("div", class_="lyrics-table")

  stanza_elems = element.find_all("p")
  
  stanzas = ''
  for stanza in stanza_elems:
    stanza = stanza.text  # Ditch the <p></p> tags
    stanzas = stanzas + stanza # Add the stanza to the overall lyrics
  
  if id_mode: # if user just wants an ID
    title = title[7:]   # each one starts with "Lyrics:" get rid of it
    return stanzas, title

  return stanzas, None
import tweepy
import configparser
import pandas as pd
import time
import re
import subprocess
from urllib.parse import urlparse
import requests
import string
import random
import datetime
import youtube_dl
import os


# read config file
config = configparser.RawConfigParser()
config.read('config.ini')

api_key = config['twitter']['api_key']
api_key_secret = config['twitter']['api_key_secret']

access_token = config['twitter']['access_token']
access_token_secret = config['twitter']['access_token_secret']

bearer_token = config['twitter']['bearer_token']

#Connection to the Twitter api

client = tweepy.Client(bearer_token, api_key, api_key_secret, access_token, access_token_secret)

auth = tweepy.OAuth1UserHandler(api_key, api_key_secret, access_token, access_token_secret)
api = tweepy.API(auth)

#Generate a random character string for the video file

def id_generator(size=10, chars=string.ascii_uppercase + string.digits):
    
    return ''.join(random.choice(chars) for _ in range(size))

rande = id_generator()

columns = ['link']
data = []

class MyStream(tweepy.StreamingClient):
    
    def on_connect(self):
        print("You are connected to the Twitter API.")
    
    def on_tweet(self, tweet):
        
        if tweet.referenced_tweets == None:
            
            rawtext = tweet.text
            # Extract all URLs with a regular expression
            matches = re.finditer(r"https?://\S+", rawtext)
            
            for match in matches:
                
                url = match.group(0)
                # Checking the validity of the URL with urlparse()
                parsed_url = urlparse(url)
                
                if parsed_url.scheme and parsed_url.netloc:
                    
                    print("Valid URL found in string:", url)
                    response = requests.get(url)
                    valid_url = response.url
                    print("Unwrapped URL:", valid_url)
                    
                    if valid_url.find("photo") != -1:
                        
                        print("the link is a picture")
                        
                    else:
                        
                        if valid_url.find("twitter.com") != -1:
                            
                            # Creating the name of the destination folder
                            date_str = datetime.datetime.now().strftime("%Y-%m-%d")
                            # Creation of the destination folder path
                            output_dir = os.path.join(os.getcwd(), date_str)
                            
                            # Creation of the file if it does not already exist
                            if not os.path.exists(output_dir):
                                
                                os.makedirs(output_dir)
                                
                            # Update of the 'outtmpl' option for youtube-dl
                            ydl_opts = {'outtmpl': os.path.join(output_dir, id_generator() + '.mp4')}
                            
                            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                                
                                ydl.download([valid_url])
                                
                            print("Download complete")
                            
                        else:
                            
                            print("Not a twitter link")

                            data.append([valid_url])
                                
                            df = pd.DataFrame(data, columns=columns)

                            print(df)
                            df.to_csv(rande+'.csv')
                    
                else:
                    
                    print("Invalid URL found in string:", url)
                    
            else:
                
                print("No URL found in string")
                
            date = datetime.datetime.now()
            print(date)
            time.sleep(0.5)

#-----------------

search_terms = []

def menu():
    
    print("1. View saved search terms")
    print("2. Add new search terms")
    print("3. Delete all search terms")
    print("4. Launch the main program")
    choice = input("Make your choice: ")
    
    if choice == "1":
        
        display_terms()
        
    elif choice == "2":
        
        add_terms()
        
    elif choice == "3":
        
        delete_terms()
        
    elif choice == "4":
        
        main_program()
        
    else:
        
        print("Invalid choice, please try again.")
        menu()

def display_terms():
    
    stream = MyStream(bearer_token=bearer_token)
    list = []
    list = stream.get_rules() # get all rules
    print(list)
    menu()

def add_terms():
    
    stream = MyStream(bearer_token=bearer_token)
    search_terms = []
    new_term = input("Enter the new search term: ")
    search_terms.append(new_term)
    
    for term in search_terms:
        
        stream.add_rules(tweepy.StreamRule(term))
        
    print("Term successfully added.")
    menu()

def delete_terms():
    
    stream = MyStream(bearer_token=bearer_token)
    list = []
    list = stream.get_rules() # get all rules
    
    try:
        
        for delet in list:   
            stream.delete_rules(delet) # delete all rules
            
    except tweepy.errors.BadRequest as e:
        
        print("All rules have been successfully removed")
        menu()

def main_program():
    
    stream = MyStream(bearer_token=bearer_token)
    list = []
    list = stream.get_rules() # get all rules
    print(list)
    
    for term in search_terms:
        
        stream.add_rules(tweepy.StreamRule(term))

    stream.filter(tweet_fields=["referenced_tweets"])

menu()


#-----------------
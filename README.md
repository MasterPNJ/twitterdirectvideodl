# twitterdirectvideodl

[![v2](https://img.shields.io/endpoint?url=https%3A%2F%2Ftwbadges.glitch.me%2Fbadges%2Fv2)](https://developer.twitter.com/en/docs/twitter-api)

## How to use the program

1. You need access to the tweeter API with preferably "Elevated" access to use this program. And create an application. I do not explain how to do this step, there is plenty of information on the internet and directly on the developer portal of twitter. https://developer.twitter.com/en
2. You need to have python installed on your computer. I used python 3.11.0. https://www.python.org/downloads/
3. You need to download the program. You can either download the zip file or clone the repository.
4. You need to install all the necessary libraries which are :
```
    pip install tweepy
    pip install configparser
    pip install pandas
    pip install time
    pip install re
    pip install subprocess
    pip install urlparse
    pip install requests
    pip install string
    pip install random
    pip install datetime
    pip install youtube_dl
    pip install os
```
5. Replace what is marked in config.ini by putting your own keys.
6. Run the program with : python .\twittersave.py
7. Use the menu to add, delete, view and/or run the program

## Information

This code is a Twitter streamer that extracts URLs from tweets, checks their validity, and downloads Twitter videos using youtube_dl. It also allows the user to add, delete, and view search terms for the Twitter stream.

Use this in accordance with the rules of the Twitter Terms of Use. https://developer.twitter.com/en/developer-terms

    

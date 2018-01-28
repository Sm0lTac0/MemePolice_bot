# Fill your Reddit and Telegram API in example.config.py and rename it to config.py
from PIL import Image
from message import message
from text_recognition import text_recognition
from tqdm import tqdm
import pytesseract
import config
import praw
import cv2
import os, sys
import urllib
import time


reddit = praw.Reddit(client_id = config.client_id,
                     client_secret = config.client_secret,
                     username = config.username,
                     password = config.password,
                     user_agent = config.user_agent)

subreddit = reddit.subreddit('PewdiepieSubmissions')

banned = ["399","chair","tide","pods","do you know","but can you do this","the way","uganda","noodle","but can","slippy","you do this","skiddadle","skadoodle","upvote if", "upvote so", "upvote to"]

def search_meme(illegal_meme, creds, selected_submission):
    if illegal_meme in creds:
        print("Found an illegal meme!")
        selected_submission.reply(message)
        print("I will wait 5 minutes as a cooldown.")
        time.sleep(300)
        return

def ban(post, recognized_text, desc):
    for word in banned:
    #    search_meme(word, recognized_text, post);
     #   return
       if word in recognized_text:
           print("Found an illegal meme!")
           post.reply(message)
           print("Will w8 1 min")
           time.sleep(60)
           return
       if word in desc:
           print("Found an illegal meme!")
           post.reply(message)
           print("Will w8 1 min")
           time.sleep(60)
           return     

def detect(post):
    if "png" or "jpg" in post.url:
        submission_id = post.id_from_url(post.shortlink)
        submission_title = post.title.encode('utf-8')
        urllib.urlretrieve(post.url, filename=submission_title)
        print(post)
        print(post.url)
        image = cv2.imread(submission_title)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        gray = cv2.medianBlur(gray, 3)
        filename = "{}-TEST.png".format(submission_title)
        cv2.imwrite(filename, gray)
        img = Image.open(filename)
        recognized_text = pytesseract.image_to_string(img).encode('utf-8').lower()
        os.remove(filename)
        os.remove(submission_title)
        print(recognized_text)
        ban(post, recognized_text, submission_title)
        
while 1:        
    for submission in tqdm(subreddit.stream.submissions()):
        print("\nStarting new meme!")
        post = reddit.submission(submission)
        title = post.title.encode('utf-8').lower()
        print("Submission title -> {}".format(title))
        if "png" in post.url:
            meme_text = text_recognition(post)
            print("Meme text -> \n {}".format(meme_text))
            ban(post, meme_text, title)
            continue
        elif "jpg" in post.url:
            meme_text = text_recognition(post)
            print("Meme text -> \n {}".format(meme_text))
            ban(post, meme_text, title)
            continue
        print("Finished this one!")
        
    time.sleep(50)

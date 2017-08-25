from tkinter import *
from tkinter import ttk
from newsapi import NewsAPI
from textblob import TextBlob
from PIL import Image
import speech_recognition as sr
from time import ctime
import time
import os
from os.path import join
from gtts import gTTS
import pyglet
import webbrowser
import numpy as np
import urllib.request
import calendar
import re
import logging
import yahooweather
from yahooweather import UNIT_C
from geopy.geocoders import Nominatim
import json
from newsapi import NewsAPI



#check connection
def interneton():
    try:
        response=urllib.request.urlopen('http://www.google.com',timeout=20)
        return True
    except urllib.error.URLError as err: pass
    return False



#say
def speak(audioString):
    #print(audioString)
    tts = gTTS(text=audioString, lang='en')
    tts.save("audio.mp3")
    filename="audio.mp3"

    music = pyglet.media.load(filename, streaming=False)
    music.play()

    time.sleep(music.duration) #prevent from killing
    os.remove(filename) #remove temperory file
     

# Record Audio
def recordAudio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)
 
    # Speech recognition using Google Speech Recognition
    data = ""
    try:
        
        data = r.recognize_google(audio)
        print("You said: " + data)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
 
    return data
 
#main
def ai(data):
    #greet
    if "how are you" in data:
        speak('I am fine')
        gui('I am fine')
        
 
    #time
    elif any(x in data for x in c):
        speak(ctime())
        gui(ctime())
        
 
    #location
    elif "where is" in data:
        data = data.split(" ")
        location = data[2]
        print("Hold on, I will show you where " + location + " is.")
        speak("Hold on, I will show you where " + location + " is.")
        
        webbrowser.open('https://www.google.co.in/maps/place/{}'.format(location), new=2) 
        time.sleep(10)
    #website
    elif "open" and "browser" in data:
        data = data.split(" ")
        site=data[1]
        print("Hold on, I will open " + site)
        speak("Hold on, I will open " + site)
        webbrowser.open('https://www.{}.com'.format(site), new=2)
        time.sleep(10)

    
    #solve
    elif 'solve' in data:
        try:
            data=data.split('solve',1)
            k=data[1].replace(' x ','*')
            k=k.replace('raise to power','**')
            speak('the solution is '+str(eval(k)))
            gui('The soluton is '+str(eval(k)))
        except Exception as e:
            print(e)
            time.sleep(5)


    #news
    elif 'news' in data:
        params = {}
        api = NewsAPI('a7d10f7638cc4644a05cf344401a81fd')

        #india

        news_str='India\n'
        articles = api.articles('the-times-of-india', params)
        for i in articles:
            analysis=TextBlob(i['title'])
            news_str=news_str+'-'+i['title']
            if analysis.sentiment.polarity < 0:
                news_str=news_str+' :(\n'
            elif analysis.sentiment.polarity > 0:
                news_str=news_str+' :)\n'
            else:
                news_str=news_str+' :|\n'
                
        #world
        news_str=news_str+"\nWorld\n"
        articles = api.articles('bbc-news', params)
        for i in articles:
            analysis=TextBlob(i['title'])
            news_str=news_str+'-'+i['title']
            if analysis.sentiment.polarity < 0:
                news_str=news_str+' :(\n'
            elif analysis.sentiment.polarity > 0:
                news_str=news_str+' :)\n'
            else:
                news_str=news_str+' :|\n'
        gui(news_str)
'''
       
    #calender
    elif 'calendar' in data:
        
        m = {'January': 1,'February': 2,'March': 3,'April':4,'May':5,'June':6,'July':7,'August':8,'September':9,'October':10,'November':11,'December':12}
        speak('which year')
        k=recordAudio()
        speak('which month')
        y=recordAudio()
        num=1

        while k=="" or y=="":
            print('Enter correct values')
            num=num+1
            if num==4:
                break
            else:
                
                speak('which year')
                k=recordAudio()
                speak('which month\n')
                y=recordAudio()

        try:
            calendar.prmonth(int(k),m[y])
        except Exception as e:
            print(e)
            print('start again\n')
            time.sleep(5)

'''
    #dictation
    elif 'start' and 'dictation' in data:
        file = open('Dictation.txt','w')
        num=0
        speak("start")
        data=recordAudio()
        while data=='':
            print('Dictation has started')
            num=num+1
            if num==4:
                break
            else:
                print('Dictation has started')
                data=recordAudio()
                
        try:
            k=data.replace(' full stop','.')
            rtn = re.split('([.!?] *)', k)
            final = ''.join([i.capitalize() for i in rtn])
            file.write(final)
            file.close()
            speak('Dictation complete.File is updated\n')
        except Exception as e:
            print(e)
            print('Start again\n')
            time.sleep(5)
    #find
    elif "find" and 'file' in data:
        data=data.replace(' dot ','.')
        
        data=data.split(" ")
        k=data.index('file')
        j=''
        for i in range(k+1,len(data)):
            j=j+data[i]

        lookfor =j.lower()
        
        speak("Searching for lower case")
        d=False
        for root, dirs, files in os.walk('C:\\'):
    
            if lookfor in files:
                speak('File Found')
                d=True
                gui("found: %s" % join(root, lookfor))
                break
        if d==False:
            speak('File not found\n')
            time.sleep(5)

    #weather
    elif 'weather' in data:
        data=data.split(' ')
        k=data.index('weather')
        city=data[k+2]
        geolocator = Nominatim()
        location = geolocator.geocode(city)
        logging.basicConfig(level=logging.WARNING)

        yweather = yahooweather.YahooWeather(yahooweather.get_woeid(location.latitude,location.longitude), UNIT_C)
        if yweather.updateWeather():
           
            
            data = yweather.Now
            
            speak('The temperature is '+data['temp']+' degree celcius.'+' Condition is '+data['text'])
            gui('The temperature is '+data['temp']+' degree celcius.'+' Condition is '+data['text'])

            
        else:
            print("Can't read data from yahoo!\n")
            time.sleep(5)
        

    #jokes
    elif 'a joke' in data:
        req = urllib.request.Request("http://api.icndb.com/jokes/random")
        full_json = urllib.request.urlopen(req).read()
        full = json.loads(full_json)
        speak('Ive got one. '+full['value']['joke'])
        gui('Ive got one. '+full['value']['joke'])


    #google search
    elif any(x in data for x in a):
        data = data.split(" ")
        search=''
        
        p=len(data)
        for i in range(2,p):
            search=search+"+"+data[i]
        print("Hold on, I will google it ")
        speak("Hold on, I will google it ")
        webbrowser.open('https://www.google.co.in/search?q={}'.format(search), new=2)
        time.sleep(10)
            
    #default
    else:
        speak('Sorry, did not get it\n')


def gui(info):
    root = Tk()

    root.title("ASSIST!")
    root.configure(background='#272A2F')
    root.geometry("400x630+1110+70")

    image = PhotoImage(file='avatar.gif')
    smaller_image = image.subsample(5,5)
    image1 = PhotoImage(file='download.png')
    smallerimage = image1.subsample(7,7)

    title=Label(root,text="ASSIST!",font="Terminal 25 bold")
    title.config(foreground="#45D4FE",background='#272A2F')
    title.pack(pady=15)

    framex=Label(root,height=30,bg='#272A2F',image=smaller_image)
    framex.pack(padx=15)

    frame1=Text(root,wrap=WORD,foreground="#0AF208",bg='#2E3337',font="Georgia 12",height=40,width=45,borderwidth=2, relief="sunken")
    frame1.insert(INSERT,info)
    frame1.pack(pady=10)
    
    
    root.mainloop()        

# initialization
if interneton():
    time.sleep(2)
    print("Hi, what can I do for you?")
    speak("Hi, what can I do for you?")
    a=['search for','what is','who is']
    b=['bye','thanks','thank you']
    c=['what time is it','what is the time']
    d=0
    data = recordAudio()
    ai(data)
    while 1:
        print('Anything else?')
        speak('Anything else?')
        data = recordAudio()
        if data=='':
            d=d+1
            if d==3:
                speak('Goodbye')
                break
        else:
            d=0
        if any(x in data for x in b):
            speak('Goodbye')
            break
        
        ai(data)
else:
    print('No Internet connection')
#np.array(['search for','what is','who is'])
#print(np)

from gtts import gTTS
import speech_recognition as sr
import os
import sys
import re
import webbrowser
import urllib
import urllib.request
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
import wikipedia
from time import strftime


def myCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        tts = gTTS(text='Say something', lang='en')
        tts.save('reco.mp3')
        os.system("mpg123 reco.mp3")
        print("Say something...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)

    try:
        command = r.recognize_google(audio).lower()
        print('You said: ' + command + '\n')

    except sr.UnknownValueError:
        print('....')
        command = myCommand();

    return command


def xylonResponse(audio):
    print(audio)
    for line in audio.splitlines():
        os.system('say' + audio)


def assistant(command):
    if 'open reddit' in command:
        reg_ex = re.search('open reddit (.*)', command)
        url = 'https://www.reddit.com/'
        if reg_ex:
            subreddit = reg_ex.group(1)
            url = url + 'r/' + subreddit
        webbrowser.open(url)
        tts = gTTS(text='The Reddit content has been opened for you Sir', lang='en')
        tts.save('red.mp3')
        os.system("mpg123 red.mp3")
        xylonResponse('The Reddit content has been opened for you Sir.')

    elif 'who are you' in command:
        tts = gTTS(text='I am Xylon, Your personal assistant', lang='en')
        tts.save('who.mp3')
        os.system("mpg123 who.mp3")

    elif 'open' in command:
        reg_ex = re.search('open (.+)', command)
        if reg_ex:
            domain = reg_ex.group(1)
            print(domain)
            url = 'https://www.' + domain
            webbrowser.open(url)
            tts = gTTS(text='The website you have requested has been opened for you Sir', lang='en')
            tts.save('web.mp3')
            os.system("mpg123 web.mp3")
            xylonResponse('The website you have requested has been opened for you Sir.')
        else:
            pass

    elif 'time' in command:
        import datetime
        now = datetime.datetime.now()
        xylonResponse('Current time is %d hours %d minutes' % (now.hour, now.minute))

    elif 'hello' in command:
        day_time = int(strftime('%H'))
        if day_time < 12:
            tts = gTTS(text='Hello Sir. Good morning', lang='en')
            tts.save('gm.mp3')
            os.system("mpg123 gm.mp3")
            xylonResponse('Hello Sir. Good morning')
        elif 12 <= day_time < 18:
            tts = gTTS(text='Hello Sir. Good afternoon', lang='en')
            tts.save('ga.mp3')
            os.system("mpg123 ga.mp3")
            xylonResponse('Hello Sir. Good afternoon')
        else:
            tts = gTTS(text='Hello Sir. Good evening', lang='en')
            tts.save('ge.mp3')
            os.system("mpg123 ge.mp3")
            xylonResponse('Hello Sir. Good evening')  # to terminate the program

    elif 'shutdown' in command:
        tts = gTTS(text='See you later, Have a nice day', lang='en')
        tts.save('bye.mp3')
        os.system("mpg123 bye.mp3")
        xylonResponse('See you later, Have a nice day')
        sys.exit()

    elif 'news for today' in command:
        try:
            news_url = "https://news.google.com/news/rss"
            Client = urlopen(news_url)
            xml_page = Client.read()
            Client.close()
            soup_page = soup(xml_page, "xml")
            news_list = soup_page.findAll("item")
            for news in news_list[:15]:
                xylonResponse(news.title.text.encode('utf-8'))
        except Exception as e:
            print(e)

    elif 'tell me about' in command:
        reg_ex = re.search('tell me about (.*)', command)
        try:
            if reg_ex:
                topic = reg_ex.group(1)
                ny = wikipedia.page(topic)
                xylonResponse(ny.content[:500].encode('utf-8'))
        except Exception as e:
            xylonResponse(e)

    elif 'hey' in command:
        tts = gTTS(text='Hey there!! How are you doing?', lang='en')
        tts.save('bye.mp3')
        os.system("mpg123 bye.mp3")

    elif 'who are you?' in command:
        tts = gTTS(text='My name is Xylon, I am your personal assistant.', lang='en')
        tts.save('who.mp3')
        os.system("mpg123 who.mp3")

    elif 'play music' in command:
        tts = gTTS(text='Playing Soap by Melanie Martinez... ')
        tts.save('music.mp3')
        os.system("mpg123 music.mp3")
        url = ("https://www.youtube.com/watch?v=ElVp4bewncs")
        webbrowser.open(url)


while True:
    assistant(myCommand())

#################################################compatible only with python3.7###########################################################################
import os
##################################################checking_dependencies#####################################################################################

while True:
    check=input('Is this your first time starting this program? Type "yes" or "no":')
    if check=="yes":
        #fixed bug and module errors
        import pip
        import subprocess
        import sys
    
        def spacyinstall(package):
            subprocess.check_call([sys.executable, "-m", "spacy", "download", package])
    
        def install(package):
            if hasattr(pip, 'main'):
                pip.main(['install', package])
            else:
                pip._internal.main(['install', package])
    
        install('nltk')
        install('pygame')
        install('spacy==2.2')
        spacyinstall('en')
        install('cleverbot_free')
        install('googletrans==3.1.0a0')
        os.system("sudo apt-get install portaudio19-dev python-pyaudio")
        install("pyaudio")
        install("ibm_watson")
        install("playsound")
        os.system("sudo apt-get install python3-tk")
        install("tkinter")
        install("wave")
        install("SpeechRecognition")
        install("wikipedia")
        break
    elif check=="no":
        break
    else:print("input not understand. Please retype your answer.")

##########################################################################modules############################################################################ 
'''
image-m
response-m
insert-m
enter button-b
record button-b
'''
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from playsound import playsound
import tkinter as tk
import threading
import pyaudio
import wave
import speech_recognition as sr
import wikipedia
from cleverbot_free.cbaio import CleverBot
import pickle
import re, string
import nltk
from googletrans import Translator
from PIL import ImageTk,Image
url='https://api.kr-seo.text-to-speech.watson.cloud.ibm.com/instances/fb3dc777-b259-4d1f-a43b-9ae80e671288'
apikey='hUNVIDkm_2Gt4HcD3oo4oOArnQYUKK3evKfxMJY2lDtB'
authenticator=IAMAuthenticator(apikey)
tts=TextToSpeechV1(authenticator=authenticator)
tts.set_service_url(url)
r = sr.Recognizer()
x=[0]
translator = Translator()
f = open(r'finalemotiondetector.pickle', 'rb')
classifier = pickle.load(f)
f.close()

from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.response_selection import get_random_response

BankBot = ChatBot(name = 'BankBot',
                  read_only = True,                  
                  logic_adapters = [
        {
            "import_path": "chatterbot.logic.BestMatch",
            'response_selection_method': get_random_response,
        },
            "chatterbot.logic.MathematicalEvaluation"],                 
                  storage_adapter = "chatterbot.storage.SQLStorageAdapter")

corpus_trainer = ChatterBotCorpusTrainer(BankBot)

def remove_noise(tweet_tokens, stop_words = ()):

    cleaned_tokens = []

    for token, tag in nltk.tag.pos_tag(tweet_tokens):
        token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'\
                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+','', token)
        token = re.sub("(@[A-Za-z0-9_]+)","", token)

        if tag.startswith("NN"):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'

        lemmatizer = nltk.stem.wordnet.WordNetLemmatizer()
        token = lemmatizer.lemmatize(token, pos)

        if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
            cleaned_tokens.append(token.lower())
    return cleaned_tokens

def lemmatize_sentence(tokens):
    lemmatizer = nltk.stem.wordnet.WordNetLemmatizer()
    lemmatized_sentence = []
    for word, tag in nltk.tag.pos_tag(tokens):
        if tag.startswith('NN'):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'
        lemmatized_sentence.append(lemmatizer.lemmatize(word, pos))
    return lemmatized_sentence

def analyse(custom_tweet):
    custom_tokens = remove_noise(nltk.tokenize.word_tokenize(custom_tweet))
    return classifier.classify(dict([token, True] for token in custom_tokens))

def wikisearch(query):
    try:
        return wikipedia.summary(query)
    except Exception:
        for new_query in wikipedia.search(query):
            try:
                return wikipedia.summary(new_query)
            except Exception:
                pass
    return "I don't know about "+query

class App():
    chunk = 1024
    sample_format = pyaudio.paInt16
    channels = 2
    fs = 44100  
   
    frames = []  
    def __init__(self, master):
        self.isrecording = False
        self.button1 = tk.Button(window, text='rec',command=self.startrecording)
        self.button2 = tk.Button(window, text='stop',command=self.stoprecording)
     
        self.button1.grid(row=5,column=0,sticky='NESW')
        self.button2.grid(row=5,column=1,sticky='NESW')

    def startrecording(self):
        self.p = pyaudio.PyAudio()  
        self.stream = self.p.open(format=self.sample_format,channels=self.channels,rate=self.fs,frames_per_buffer=self.chunk,input=True)
        self.isrecording = True
       
        print('Recording')
        t = threading.Thread(target=self.record)
        t.start()

    def stoprecording(self):
        self.isrecording = False
        print('recording complete')
        self.filename='testvoice'
        self.filename = self.filename+".wav"
        wf = wave.open(self.filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.p.get_sample_size(self.sample_format))
        wf.setframerate(self.fs)
        wf.writeframes(b''.join(self.frames))
        wf.close()
        mainai(x)
    def record(self):
       
        while self.isrecording:
            data = self.stream.read(self.chunk)
            self.frames.append(data)

def mainai(x):
    text=''
    try:
        with sr.AudioFile('testvoice.wav') as source: audio=r.record(source)
        current=r.recognize_google(audio).split()
        for i in range(x[0]):
            del current[0]
        x[0]+=len(current)
        print("You say: "+' '.join(current))
        text=' '.join(current)
        user_input=False
        os.remove('testvoice.wav')
    except:
        print("Voice recognization failed. Please type or retry.")
        response.configure(text="Voice recognization failed. Please type or retry.")
        return
   
    if (text == 'quit'):
        window.destroy()
    elif (text == ''):
        print("Voice recognization failed. Please type or retry.")
        response.configure(text="Voice recognization failed. Please type or retry.")
        return
    elif text[0:4]=='wiki':
        restext=wikisearch(text.lstrip('wiki '))
    else: restext = BankBot.get_response(text)
   
    print (analyse(str(translator.translate(str(restext), dest='en').text)))
    if str(restext)[-1]=='.' or str(restext)[-1]=='?' or str(restext)[-1]=='!':
        img = ImageTk.PhotoImage(Image.open("emotions/"+analyse(str(translator.translate(str(restext), dest='en').text))+".png"))
        image.configure(image=img)
        image.image=img
        print('AI-Serve says: '+str(restext))
        response.configure(text=str(restext))
       
    with open('voice.mp3','wb') as audio_file:
        res=tts.synthesize(str(restext),accept='audio/mp3',voice='en-US_AllisonVoice').get_result()
        audio_file.write(res.content)
    playsound("voice.mp3")
    os.remove("voice.mp3")
    x[0]=x[0]
           
def respond():
    text=entry1.get()
    if (text == 'quit'):
        window.destroy()
    elif (text == ''):
        print("Unknown input. Please use voice recognization or retype.")
        response.configure(text="Unknown input. Please use voice recognization or retype.")
        return
    elif text[0:4]=='wiki':
        restext=wikisearch(text.lstrip('wiki '))
    else: restext = BankBot.get_response(text)
   
    print (analyse(str(translator.translate(str(restext), dest='en').text)))
    if str(restext)[-1]=='.' or str(restext)[-1]=='?' or str(restext)[-1]=='!':
        img = ImageTk.PhotoImage(Image.open("emotions/"+analyse(str(translator.translate(str(restext), dest='en').text))+".png"))
        image.configure(image=img)
        image.image=img
        print('AI-Serve says: '+str(restext))
        response.configure(text=str(restext))
       
    with open('voice.mp3','wb') as audio_file:
        res=tts.synthesize(str(restext),accept='audio/mp3',voice='en-US_AllisonVoice').get_result()
        audio_file.write(res.content)
    playsound("voice.mp3")
    os.remove("voice.mp3")

print("initialising...")

window= tk.Tk()
window.title("AI_Serve the Companion Bot")

img = ImageTk.PhotoImage(Image.open("emotions/normal.png"))
image = tk.Label(window, image=img)
image.grid(row=1,columnspan=2,sticky='NESW')

button1 = tk.Button(window,text='Enter', command=respond).grid(row=4,columnspan=2,sticky='NESW')

response = tk.Label(window, text="Type Something to Chat")
response.grid(row=2,columnspan=2,sticky='NESW')

entry1 = tk.Entry (window)
entry1.grid(row=3,columnspan=2,sticky='NESW')

App(window)

window.mainloop()

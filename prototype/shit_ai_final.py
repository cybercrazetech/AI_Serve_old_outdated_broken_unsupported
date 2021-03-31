#gTTS, playsound, pyttsx3
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
        install('chatterbot')
        install('playsound')
        install('ibm_watson')
        os.system("sudo apt-get install python3-tk")
        install("tkinter")
        install("wave")
        install("SpeechRecognition")
        install("wikipedia")
        os.system("sudo apt-get install portaudio19-dev python-pyaudio")
        install("pyaudio")
        break
    elif check=="no":
        break
    else:print("input not understood. Please retype your answer.")

url='https://api.kr-seo.text-to-speech.watson.cloud.ibm.com/instances/fb3dc777-b259-4d1f-a43b-9ae80e671288'
apikey='hUNVIDkm_2Gt4HcD3oo4oOArnQYUKK3evKfxMJY2lDtB'
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import pickle
import re, string
import nltk
import pygame
import os
import wikipedia
from playsound import playsound
import tkinter as tk
import threading
import pyaudio
import wave
import speech_recognition as sr
from googletrans import Translator
translator = Translator()

authenticator=IAMAuthenticator(apikey)
tts=TextToSpeechV1(authenticator=authenticator)
tts.set_service_url(url)

r = sr.Recognizer()
x=0

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

f = open(r'finalemotiondetector.pickle', 'rb')
classifier = pickle.load(f)
f.close()

class App():
    chunk = 1024 
    sample_format = pyaudio.paInt16 
    channels = 2
    fs = 44100  
    
    frames = []  
    def __init__(self, master):
        self.isrecording = False
        self.button1 = tk.Button(main, text='rec',command=self.startrecording)
        self.button2 = tk.Button(main, text='stop',command=self.stoprecording)
      
        self.button1.pack()
        self.button2.pack()

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
        main.destroy()
    def record(self):
       
        while self.isrecording:
            data = self.stream.read(self.chunk)
            self.frames.append(data)

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

####
pygame.init()

SIZE = WIDTH, HEIGHT = (600, 900)
#font = pygame.font.Font('freesansbold.ttf',32)
#font = pygame.font.SysFont('Arial',32)
font = pygame.font.Font('Cyberbit.ttf',32)
screen = pygame.display.set_mode(SIZE, pygame.RESIZABLE)

def centre_text(array,font,surface,y, color=pygame.Color('black')):
    finalstring=''
    for arrays in array:
        finalstring+=arrays
    finalrender = font.render(finalstring, 0, color)
    final_rect = finalrender.get_rect(center=(600/2, y))
    surface.blit(finalrender, final_rect)

def blit_text(surface, text, pos, font, color=pygame.Color('black')):
    words = text.split(' ')
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    x, y = pos
    array=[]
    for word in words:
        word_surface = font.render(word, 0, color)
        word_width, word_height = word_surface.get_size()
        if x + word_width >= max_width-space:
           x = pos[0]  # Reset the x.
           y += word_height  # Start on new row.
           centre_text(array,font,surface,y)
           array=[]
        array.append(word+' ')
        x += word_width + space
    if x < max_width-space:
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.
        centre_text(array,font,surface,y)
        array=[]

image = pygame.image.load("emotions/normal.png").convert()
response=''
while (True):
    pygame.event.get()
    screen.fill((255,255,255))
    screen.blit(image, (80,150))
    if response=='':
        blit_text(screen, 'Start the conversation', (10, 650), font)
    else:
        blit_text(screen, str(response), (10, 650), font)
        pygame.display.update()
        with open('voice.mp3','wb') as audio_file:
            res=tts.synthesize(str(response),accept='audio/mp3',voice='en-US_AllisonVoice').get_result()
            audio_file.write(res.content)
        playsound("voice.mp3")
        os.remove("voice.mp3")

    if pygame.event.get(pygame.QUIT):
        break
    pygame.display.update()

    main = tk.Tk()
    main.title('recorder')
    main.geometry('200x50')
    app = App(main)
    main.mainloop()
    try:
        with sr.AudioFile('testvoice.wav') as source: audio=r.record(source)
        current=r.recognize_google(audio).split()
        for i in range(x):
            del current[0]
        x+=len(current)
        print("You say: "+' '.join(current))
        user_input=' '.join(current)
        os.remove('testvoice.wav')
    except:
        print("Voice recognization failed. Please type.")
        user_input=input("You say: ")
    if (user_input == 'quit'):
        break
    elif (user_input == ''):
        print("Voice recognization failed. Please type.")
        user_input=input("You say: ")
    if user_input[0:4]=='wiki':
        response=wikisearch(user_input.lstrip('wiki '))
    else: response = BankBot.get_response(user_input)
    print (analyse(str(response)))
    image = pygame.image.load("emotions/"+analyse(str(response))+".png").convert()
    screen.blit(image, (80,150))
    print (response)
    pygame.display.update()

pygame.quit()

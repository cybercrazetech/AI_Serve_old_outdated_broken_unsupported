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
import pygame
from googletrans import Translator
url='https://api.kr-seo.text-to-speech.watson.cloud.ibm.com/instances/fb3dc777-b259-4d1f-a43b-9ae80e671288'
apikey='hUNVIDkm_2Gt4HcD3oo4oOArnQYUKK3evKfxMJY2lDtB'
authenticator=IAMAuthenticator(apikey)
tts=TextToSpeechV1(authenticator=authenticator)
tts.set_service_url(url)
r = sr.Recognizer()
x=0
translator = Translator()
f = open(r'finalemotiondetector.pickle', 'rb')
classifier = pickle.load(f)
f.close()

##############################################################function#########################################################################################

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

####################################################code#######################################################################

print("modules loaded")

cb = CleverBot()

pygame.init()

SIZE = WIDTH, HEIGHT = (600, 900)

#font = pygame.font.SysFont('Arial',32)
font = pygame.font.Font('Cyberbit.ttf',32)

screen = pygame.display.set_mode(SIZE, pygame.RESIZABLE)
pygame.display.set_caption("AI_Serve")
response=''

print('restarting...')
cb.init()
print("cleverbot initialised")
while True:
    pygame.event.get()
    screen.fill((255,255,255))
    if response=='':
       image = pygame.image.load("emotions/normal.png").convert()
       screen.blit(image, (80,150))
       blit_text(screen, 'Start the Conversation', (10, 650), font)
       pygame.display.update()
    else:
       screen.blit(image, (80,150))
       blit_text(screen, str(response), (10, 650), font)
       pygame.display.update()
       with open('voice.mp3','wb') as audio_file:
            res=tts.synthesize(str(response),accept='audio/mp3',voice='en-US_AllisonVoice').get_result()
            audio_file.write(res.content)
       playsound("voice.mp3")
       os.remove("voice.mp3")

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
        text=' '.join(current)
        os.remove('testvoice.wav')
    except:
        print("Voice recognization failed. Please type.")
        text=input("You say: ")
    if (text == 'quit'):
        break
    elif (user_input == ''):
        print("Voice recognization failed. Please type.")
        user_input=input("You say: ")
    if text[0:4]=='wiki':
        response=wikisearch(text.lstrip('wiki '))
    else: response = cb.getResponse(text)
    print (analyse(str(translator.translate(str(response), dest='en').text)))
    if str(response)[-1]=='.' or str(response)[-1]=='?' or str(response)[-1]=='!':
        image = pygame.image.load("emotions/"+analyse(str(translator.translate(str(response), dest='en').text))+".png").convert()
        screen.blit(image, (80,150))
        pygame.display.update()
        print('AI-Serve says: '+str(response))

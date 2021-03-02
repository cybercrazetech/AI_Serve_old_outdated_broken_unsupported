from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import pickle
import re, string
import nltk
import os
import wikipedia
from playsound import playsound
from googletrans import Translator
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.response_selection import get_random_response
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivymd.app import MDApp
from kivy.uix.image import Image
url='https://api.kr-seo.text-to-speech.watson.cloud.ibm.com/instances/fb3dc777-b259-4d1f-a43b-9ae80e671288'
apikey='hUNVIDkm_2Gt4HcD3oo4oOArnQYUKK3evKfxMJY2lDtB'

translator = Translator()

authenticator=IAMAuthenticator(apikey)
tts=TextToSpeechV1(authenticator=authenticator)
tts.set_service_url(url)

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

f = open(r'finalemotiondetector.pickle', 'rb')
classifier = pickle.load(f)
f.close()

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

class MyGrid(Widget):

    def btn(self):
        print("Your input:", self.ids.user_input.text)
#####
        user_input=self.ids.user_input.text
        if user_input[0:4]=='wiki':
            response=wikisearch(user_input.lstrip('wiki '))
        else: response = BankBot.get_response(user_input)
        print (analyse(str(response)))
        self.ids.emotion.source = "png/"+analyse(str(response))+"2.png"
        print (response)
#####
        self.ids.response.text = str(response)
        self.ids.user_input.text = ""

    def speak(self):
        with open('voice.mp3','wb') as audio_file:
            res=tts.synthesize(self.ids.response.text,accept='audio/mp3',voice='en-US_AllisonVoice').get_result()
            audio_file.write(res.content)
        playsound("voice.mp3")
        os.remove("voice.mp3")

class AI_ServeApp(MDApp):
    def build(self):
        return MyGrid()

AI_ServeApp().run()

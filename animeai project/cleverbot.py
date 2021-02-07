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
        break
    elif check=="no":
        break
    else:print("input not understand. Please retype your answer.")

from cleverbot_free.cbaio import CleverBot
import pickle
import re, string
import nltk
import pygame

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

print("modules loaded")

cb = CleverBot()

pygame.init()

SIZE = WIDTH, HEIGHT = (600, 900)

#font = pygame.font.SysFont('Arial',32)
font = pygame.font.Font('Cyberbit.ttf',32)

screen = pygame.display.set_mode(SIZE, pygame.RESIZABLE)

response=''

def run1(response):
    try:
        print('restarting...')
        cb.init()
        print("cleverbot initialised")
        while True:
            pygame.event.get()
            screen.fill((255,255,255))
            if response=='':
               image = pygame.image.load("emotions/normal.png").convert()
               screen.blit(image, (80,150))
               blit_text(screen, 'Type something to chat', (10, 650), font)
            else:
               screen.blit(image, (80,150))
               blit_text(screen, str(response), (10, 650), font)

            pygame.display.update()
            text = input("Say something to CleverBot:")
            response = cb.getResponse(text)
            print (analyse(str(response)))
            if str(response)[-1]=='.' or str(response)[-1]=='?':
                image = pygame.image.load("emotions/"+analyse(str(response))+".png").convert()
                screen.blit(image, (80,150))
                pygame.display.update()
                print('Cleverbot says: '+str(response))
    except:run2(str(response))

def run2(response):
    try:
        print('restarting...')
        cb.init()
        print("cleverbot initialised")
        while True:
            pygame.event.get()
            screen.fill((255,255,255))
            if response=='':
               image = pygame.image.load("emotions/normal.png").convert()
               screen.blit(image, (80,150))
               blit_text(screen, 'Type something to chat', (10, 650), font)
            else:
               screen.blit(image, (80,150))
               blit_text(screen, str(response), (10, 650), font)

            pygame.display.update()
            text = input("Say something to CleverBot:")
            response = cb.getResponse(text)
            print (analyse(str(response)))
            if str(response)[-1]=='.' or str(response)[-1]=='?':
                image = pygame.image.load("emotions/"+analyse(str(response))+".png").convert()
                screen.blit(image, (80,150))
                pygame.display.update()
                print('Cleverbot says: '+str(response))
    except:run1(str(response))

run1(response)


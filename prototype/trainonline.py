'''
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
from cleverbot_free.cbaio import CleverBot

cb = CleverBot()
cb.init()

BankBot = ChatBot(name = 'BankBot',
                  read_only = False,                  
                  logic_adapters = ["chatterbot.logic.BestMatch"],                 
                  storage_adapter = "chatterbot.storage.SQLStorageAdapter")

corpus_trainer = ChatterBotCorpusTrainer(BankBot)
#corpus_trainer.train("chatterbot.corpus.english")

response2='Hi.'
print('Cleverbot says: Hi.')
response1 = BankBot.get_response(str(response2))
print('Chatterbot says: '+str(response1))
while True:
    response2 = cb.getResponse(str(response1))
    if str(response2)[-1]=='.' or str(response2)[-1]=='?':
        print('Cleverbot says: '+str(response2))
        response1 = BankBot.get_response(str(response2))
        print('Chatterbot says: '+str(response1))
'''
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
from cleverbot_free.cbaio import CleverBot
import random

cb = CleverBot()

BankBot = ChatBot(name = 'BankBot',
                  read_only = False,                  
                  logic_adapters = ["chatterbot.logic.BestMatch"],                 
                  storage_adapter = "chatterbot.storage.SQLStorageAdapter")

corpus_trainer = ChatterBotCorpusTrainer(BankBot)
#corpus_trainer.train("chatterbot.corpus.english")
starting=['Hi.',"What's up? bro.","Hello.","Jesus! Who are you?",'Hello!','Good morning.','Good afternoon.','Good evening.',"It's nice to meet you.","It's a pleasure to meet you.",'Morning!']

def run1():
    try:
        start=random.choice(starting)
        print('restarting...')
        cb.init()
        response2=start
        print('Cleverbot says: '+start)
        response1 = BankBot.get_response(str(response2))
        print('Chatterbot says: '+str(response1))
        while True:
            response2 = cb.getResponse(str(response1))
            if str(response2)[-1]=='.' or str(response2)[-1]=='?':
                print('Cleverbot says: '+str(response2))
                response1 = BankBot.get_response(str(response2))
                print('Chatterbot says: '+str(response1))
    except:run2()

def run2():
    try:
        start=random.choice(starting)
        print('restarting...')
        cb.init()
        response2=start
        print('Cleverbot says: '+start)
        response1 = BankBot.get_response(str(response2))
        print('Chatterbot says: '+str(response1))
        while True:
            response2 = cb.getResponse(str(response1))
            if str(response2)[-1]=='.' or str(response2)[-1]=='?':
                print('Cleverbot says: '+str(response2))
                response1 = BankBot.get_response(str(response2))
                print('Chatterbot says: '+str(response1))
    except:run1()

run1()

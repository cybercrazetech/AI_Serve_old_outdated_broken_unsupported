from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer

BankBot = ChatBot(name = 'BankBot',
                  read_only = False,                  
                  logic_adapters = ["chatterbot.logic.BestMatch"],                 
                  storage_adapter = "chatterbot.storage.SQLStorageAdapter")

corpus_trainer = ChatterBotCorpusTrainer(BankBot)
#corpus_trainer.train("chatterbot.corpus.english")

response2='Hi'
print('Chatterbot1 says: Hi')
while(True):
    response1 = BankBot.get_response(str(response2))
    print('Chatterbot2 says: '+str(response1))
    response2 = BankBot.get_response(str(response1))
    print('Chatterbot1 says: '+str(response2))

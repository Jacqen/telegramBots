# -*- coding: utf-8 -*-
import telegram
import logging
import random
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
token = '1359708375:AAFqmdoheGs3qZFbC22bAUCFgvSr-D-vwOw'  ##testbot
tokenv = '1268778992:AAHXF24_4ZuEqhPe9OKFVczDy54VAdTY-tg'
updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
bot = telegram.Bot(token=token)
gameRunning = False

class playerR1:
    def __init__(self, name, username, lives):
        self.name = name
        self.username = username
        self.lives = lives

players = [playerR1('test', '@talitagigi', [12, 18, 22, 26]),
            playerR1('test', '@tiagoflexa', [3, 7, 13, 27]),
            playerR1('test', '@daniestx', [9, 18, 22, 24]),
            playerR1('test', '@LeGEOnina', [2, 13, 20, 27]),
            playerR1('test', '@plsnchs', [6, 12, 20, 30]),
            playerR1('test', '@Bijuoo', [4, 6, 17, 26]),
            playerR1('test', '@karidodente', [6, 20, 24, 30]),
            playerR1('test', '@tiptopper', [8, 9, 18, 19])
           ]



class users:
    def __init__ (self, id, group):
        self.id = id
        self.group

    def __str__ (self):
        return str(self.__class__) + ": " + str(self.__dict__)


class groups:
    def __init__(self, id, senha, gameRunning, header, lobby, bingo, restaUm, restaUmLobby, wordChain, wordChainLobby):
        self.id = id
        self.senha = senha
        self.gameRunning = gameRunning
        self.guesses = []
        self.header = header
        self.lobby = lobby
        self.playerList = []

        self.headerBingo = ''
        self.bingo = bingo
        self.bingoNumbers = []
        self.rolledNumberBingo = []

        self.restaUm = restaUm
        self.restaUmLobby = restaUmLobby
        self.restaUmAdmin = 0
        self.restaUmLista = ''
        self.rerstaUmHeader = ''
        self.livesHeader = ''

        self.wordChain = wordChain
        self.worrdChainLobby = wordChainLobby
    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

groupGames = []

def rotateList(playerList):
    return playerList[1:] + playerList[:1]

def showEmojiNumber(n):
    number = ''
    if n < 10:
        number += '️0⃣'
    n = str(n)
    for char in n:
        if char == '0':
            number += '️0⃣'
        elif char == '1':
            number += '1️⃣'
        elif char == '2':
            number += '2️⃣'
        elif char == '3':
            number += '3️⃣'
        elif char == '4':
            number += '4️⃣'
        elif char == '5':
            number += '5️⃣'
        elif char == '6':
            number += '6️⃣'
        elif char == '7':
            number += '7️⃣'
        elif char == '8':
            number += '8️⃣'
        elif char == '9':
            number += '9️⃣'
    return number


def getGroupGame(chatId):
    global groupGames, groups
    for group in groupGames:
        if group.id == chatId:
            return group
    groupGames.append(groups(chatId, 0, False, 0, False, False, False, False, False, False))
    return groupGames[-1]


def isPrivate(chatID):
    if chatID < 0:
        return False
    else:
        return True

#######################  MIND GAME ######################

def start(update, context):
    global groupGames

    chatId = update.message.chat.id
    group = getGroupGame(chatId)

    if group.gameRunning and (not isPrivate(chatId)) and (not group.lobby) :
        context.bot.send_message(chat_id=update.effective_chat.id, text="Já há um jogo em andamento!")
        updater.start_polling()
    if (not group.gameRunning) and (not isPrivate(chatId)) and (not group.lobby) :
        group.gameRunning = True
        txt = 'O jogo vai começar, para entrar digite /entrar, para começar digite /comecar. Jogadores no lobby:'
        group.header = context.bot.send_message(chat_id=update.effective_chat.id, text=txt)
        group.lobby = True
    if isPrivate(chatId):
        context.bot.send_message(chat_id=update.effective_chat.id, text='Dê startmind em um grupo')

def guess(update, context):
    chatId = update.message.chat.id
    group = getGroupGame(chatId)
    playerx = group.playerList[0]
    if group.gameRunning and (not group.lobby) and playerx == update.message.from_user:
        guess = ''.join(context.args)
        #print('len guess: ' + str(len(group.senha)))
        if len(guess) != len(group.senha) or not guess.isnumeric():
            txt = 'O seu chute não tem ' + str(len((group.senha))) + ' números.'
            update.message.reply_text(txt)
        if guess in group.guesses:
            context.bot.send_message(chat_id=update.effective_chat.id, text='Este número já foi utilizado.')
        if guess not in group.guesses and len(guess) == len(group.senha) and guess.isnumeric():
            correct = 0
            for i in range(len(group.senha)):
                if group.senha[i] == guess[i]:
                    correct += 1
            guess = guess + ' - ' + str(correct)
            txt = group.header.text + '\n' + guess
            group.header.text = txt
            bot.edit_message_text(txt, chat_id=chatId, message_id=group.header.message_id, reply_markup=None)
            if guess in group.guesses:
                context.bot.send_message(chat_id=update.effective_chat.id, text='Este número já foi utilizado.')
            if guess not in group.guesses:
                group.guesses.append(guess)
                if correct > 1 and correct < len(group.senha):
                    txt = 'Você chutou ' + str(correct) + ' números corretos'
                if correct == 1:
                    txt = 'Você chutou ' + str(correct) + ' números correto.'
                if correct == 0:
                    txt = 'Você acertou nenhum número.'
                if correct == len(group.senha):
                    txt = 'Você acertou a senha! Parabéns!'
                    group.gameRunning = False
                    group.guesses = []
                    group.playerList = []
                #context.bot.send_message(chat_id=update.effective_chat.id, text=txt)
                update.message.reply_text(txt)
                if group.playerList:
                    group.playerList = rotateList(group.playerList)
                    player = group.playerList[0]
                    txt = displayPlayer(player) + ' é seu turno. Para chutar digite: \"/chutar + número\"'
                    context.bot.send_message(chat_id=update.effective_chat.id, text=txt)
    if not group.gameRunning and group.lobby:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Não há um jogo em andamento')

    updater.start_polling()

def showGuesses(update, context):
    chatId = update.message.chat.id
    group = getGroupGame(chatId)
    if group.gameRunning:
        guesses = 'Chutes: \n'
        for g in group.guesses:
            guesses = guesses + g + '\n'
        context.bot.send_message(chat_id=update.effective_chat.id, text=guesses)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Não há um jogo em andamento')

def killGame(update, context):
    chatId = update.message.chat.id
    group = getGroupGame(chatId)
    if group.gameRunning:
        group.gameRunning = False
        group.lobby = False
        group.guesses = []
        group.playerList = []
        context.bot.send_message(chat_id=update.effective_chat.id, text='O jogo foi encerrado, a senha era: ' + str(group.senha))
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Não há um jogo em andamento')

def test(update, context):
    keyboard = [[InlineKeyboardButton("Option 1", callback_data='1'),
                 InlineKeyboardButton("Option 2", callback_data='2')],

                [InlineKeyboardButton("Option 3", callback_data='3')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Please choose:', reply_markup=reply_markup)

def button(update, context):
    query = update.callback_query
    user = query.message
    print(user)
    print(query)

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()

    query.edit_message_text(text="Selected option: {}".format(query.data))

def displayPlayer(player):
    txt = ''
    if player.username:
        txt += '@' + player.username
    else:
        txt += player.first_name
        if player.last_name:
            txt += ' ' + player.last_name
    txt += ''
    return txt

def entrar(update, context):
    chatId = update.message.chat.id
    group = getGroupGame(chatId)
    if group.lobby:
        user = update.message.from_user
        if user not in group.playerList:
            group.playerList.append(user)
            txt = group.header.text + '\n' + displayPlayer(user)
            group.header.text = txt
            bot.edit_message_text(txt, chat_id=chatId, message_id=group.header.message_id, reply_markup=None)
            txt = displayPlayer(user) + ' entrou na partida.'
            context.bot.send_message(chat_id=update.effective_chat.id, text=txt)
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text='Você ja entrou.')
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Espere o proximo jogo.')

def gerarSenha(n):
    if n <= 3:
        senha = random.randint(0, 999)
        return str("{:03d}".format(senha))
    if n > 3 and n <= 5:
        senha = random.randint(0, 9999)
        return str("{:04d}".format(senha))
    if n > 5 and n <= 7:
        senha = random.randint(0, 99999)
        return str("{:05d}".format(senha))
    if n > 7 and n <= 9:
        senha = random.randint(0, 999999)
        return str("{:06d}".format(senha))
    if n > 9 and n <= 14:
        senha = random.randint(0, 9999999)
        return str("{:07d}".format(senha))
    if n > 14:
        senha = random.randint(0, 99999999)
        return str("{:08d}".format(senha))


def comecar(update, context):
    chatId = update.message.chat.id
    group = getGroupGame(chatId)
    if len(group.playerList) < 1 and group.lobby:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Não há jogadores suficientes')
    elif not group.lobby:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Ainda não foi criado um lobby, para criar mande /startmind')
    else:
        group.lobby = False
        random.shuffle(group.playerList)
        group.senha = gerarSenha(len(group.playerList))
        print('senha: ' + group.senha)
        txt = 'Senha: '
        for i in group.senha:
            txt += '🔒'
        txt += '\nOrdem dos jogadores:\n'
        for player in group.playerList:
            txt += displayPlayer(player) + '\n'
        txt = txt + '\nChutes:\n  '
        groups.gameRunning = True
        group.header = context.bot.send_message(chat_id=update.effective_chat.id, text=txt)
        player = group.playerList[0]
        txt = displayPlayer(player) + ' é seu turno. Para chutar digite: \"/chutar + número\".'
        context.bot.send_message(chat_id=update.effective_chat.id, text=txt)

###################  BINGO  ####################

def startBingo(update, context):
    chatId = update.message.chat.id
    group = getGroupGame(chatId)
    if not group.bingo:
        n = ''.join(context.args)
        if n.isnumeric():
            update.message.reply_text('Um jogo de bingo com ' + str(n) + ' números foi iniciado! Boa sorte a todos! Para sortear um número: /sortear e para encerrar a partida: /encerrarbingo')
            txt = 'Números sorteados:'
            group.headerBingo = context.bot.send_message(chat_id=update.effective_chat.id, text=txt)
            group.bingo = True
            group.bingoNumbers = []
            group.rolledNumberBingo = []
            for i in range(1, (int(n)+1)):
                group.bingoNumbers.append(i)
        else:
            update.message.reply_text('Você precisa indicar a quantidade de números do bingo, ex: /startbingo 30')
    else:
        update.message.reply_text('Já existe um jogo de bingo nesse grupo, para encerra-ló escreva /encerrarbingo')

def encerrarBingo(update, context):
    chatId = update.message.chat.id
    group = getGroupGame(chatId)
    if group.bingo:
        group.bingo = False
        group.bingoNumbers =[]
        group.rolledNumberBingo = []
        update.message.reply_text('O jogo de bingo foi encerrado')
def roll(update, context):
    chatId = update.message.chat.id
    group = getGroupGame(chatId)
    if group.bingo:
        n = random.choice(group.bingoNumbers)
        group.rolledNumberBingo.append(n)
        group.rolledNumberBingo.sort()
        group.bingoNumbers.remove(n)
        update.message.reply_text('O número sorteado foi: ' + showEmojiNumber(n))
        txt = 'Números sorteados: \n\n'
        for i in range(len(group.rolledNumberBingo)):
            if i == 0:
                txt += showEmojiNumber(group.rolledNumberBingo[i])
            elif i%5 == 0:
                txt += '\n' + showEmojiNumber(group.rolledNumberBingo[i])
            else:
                txt += '\t•\t' + showEmojiNumber(group.rolledNumberBingo[i])
        bot.edit_message_text(txt, chat_id=chatId, message_id=group.headerBingo.message_id, reply_markup=None)

def sorteados(update, context):
    chatId = update.message.chat.id
    group = getGroupGame(chatId)
    if group.bingo and len(group.rolledNumberBingo) >= 1:
        txt = 'Números sorteados: \n'
        for i in range(len(group.rolledNumberBingo)):
            if i == 0:
                txt += showEmojiNumber(group.rolledNumberBingo[i])
            elif i%5 == 0:
                txt += '\n' + showEmojiNumber(group.rolledNumberBingo[i])
                txt += '--x--x--x--x--'
            else:
                txt += '\t|\t' + showEmojiNumber(group.rolledNumberBingo[i])
        update.message.reply_text(txt)

################## RESTA UM ##################

def startRestaUm(update,    context):
    chatId = update.message.chat.id
    group = getGroupGame(chatId)
    if not group.restaUm and not isPrivate(chatId) and not group.restaUmLobby:
        group.restaUmLobby = True
        group.restaUmAdmin = update.message.from_user.id
        context.bot.send_message(chat_id=update.effective_chat.id, text='Um jogo de resta um vai começar, para adicionar jogadores o admin (quem deu /restaum)'
                                                                        ' deve mandar no pv do bot /adicionar + user + números escolhidos. Para começar o jogo mande /comecarrestaum')

def adicionar(update, context):
    chatId = update.message.chat.id
    group = getGroupGame(chatId)
    if isPrivate(chatId):
        groupId

def adicionarlista(update, context):
    chatId = update.message.chat.id
    group = getGroupGame(chatId)
    group.restaUm = ''.join(context.args)
    txt = group.restaUm + '.txt'
    try:
        f = open(txt, 'r')
        lines = f.readlines()
        f.close()
        txt = 'Resta um: ' + group.restaUm + '\n\n'
        group.restaUmLista = lines
        for line in lines:
            txt += line
        group.restaUmHeader = context.bot.send_message(chat_id=update.effective_chat.id, text=txt)
        txt = 'Ordem e Vida dos Jogadores 🐺❤️\n\n'
        for p in players:
            txt += p.username + ': '
            for l in p.lives:
                txt += '❤️'
            txt += '\n'

        group.livesHeader = context.bot.send_message(chat_id=update.effective_chat.id, text=txt)
    except:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Não foi possível encontrar a lista.')

def eliminar(update, context):
    chatId = update.message.chat.id
    group = getGroupGame(chatId)
    playerslost = []
    x = str("{:02d}".format(int(''.join(context.args))))
    try:
        for line in group.restaUmLista:
            result = line.find(x)
            if result == 0:
                group.restaUmLista.remove(line)
        txt = 'Resta um: ' + group.restaUm + '\n\n'
        for line in group.restaUmLista:
            txt += line
        bot.edit_message_text(txt, chat_id=chatId, message_id=group.restaUmHeader.message_id, reply_markup=None)
        for p in players:
            if int(x) in p.lives:
                p.lives.remove(int(x))
                playerslost.append(p.username)
                txt = p.username + ' perdeu uma vida!'
                context.bot.send_message(chat_id=update.effective_chat.id, text=txt)
                txt = 'Ordem e Vida dos Jogadores 🐺❤️\n\n'
                for p in players:
                    txt += p.username + ': '
                    for l in p.lives:
                        txt += '❤️'
                    txt += '\n'
                bot.edit_message_text(txt, chat_id=chatId, message_id=group.livesHeader.message_id, reply_markup=None)
    except:
        update.message.reply_text('Esse número já foi eliminado.')

####################HANDLERS###########################
dispatcher.add_handler(CommandHandler('test', test))
dispatcher.add_handler(CallbackQueryHandler(button))

#@@@@@@@@@@@@@@@@@@@@@ mindgame @@@@@@@@@@@@@@@@@@#
dispatcher.add_handler(CommandHandler('chutar', guess))
dispatcher.add_handler(CommandHandler('startmind', start))
dispatcher.add_handler(CommandHandler('encerrar', killGame))
dispatcher.add_handler(CommandHandler('chutes', showGuesses))
dispatcher.add_handler(CommandHandler('entrar', entrar))
dispatcher.add_handler(CommandHandler('comecar', comecar))

#@@@@@@@@@@@@@@@@@@@@@ bingo @@@@@@@@@@@@@@@@@@@@#
dispatcher.add_handler(CommandHandler('startbingo', startBingo))
dispatcher.add_handler(CommandHandler('encerrarbingo', encerrarBingo))
dispatcher.add_handler(CommandHandler('sortear', roll))
dispatcher.add_handler(CommandHandler('sorteados', sorteados))

#dispatcher.add_handler(CommandHandler('restaum', startRestaUm))
#dispatcher.add_handler(CommandHandler('adicionar', adicionar))
dispatcher.add_handler(CommandHandler('restaum', adicionarlista))
dispatcher.add_handler(CommandHandler('eliminar', eliminar))

updater.start_polling()
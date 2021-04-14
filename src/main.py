from telegram.ext import Updater, InlineQueryHandler, CommandHandler, MessageHandler, Filters
from pendulum import today, datetime
import random

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Já em funcionamento.")


def fwd(update, context):
    is_reply = update.message.reply_to_message
    fwd_name = '@becdbotfwd'
    
    if is_reply: # encaminha para o fwd
        context.bot.forwardMessage(fwd_name, update.effective_chat.id, is_reply.message_id)
    else: # encaminha para o grupo
        max_id = 10
        max_tries = max_id*5
        tries = 0
        while True:
            message_id = random.randint(0, max_id)
            try:
                if tries <= max_tries: 
                    context.bot.forwardMessage(update.effective_chat.id, fwd_name, message_id )
                    break
                    tries+=1
                else:
                    context.bot.send_message(chat_id=update.effective_chat.id, text="Ai cansei aqui, manda de novo...")
            except:
                pass
    

def aulas(update, context):
    """
    hoje = today('America/Sao_Paulo')
    aulas = datetime(2021, 4, 12)
    diff = aulas.diff(hoje).in_days()
    frases = [
        'Caalma, caraio. As aulas vão começar em',
        'Porra, bixo. As aulas começam em',
        'Infelizmente já teremos aulas em',
        'Poorrraaaa, não me lembra que as aulas começam em'
    ]
    frase = random.choice(frases)
    msg = f'{frase} {diff} dias'
    """
    msg = "As aulas já começaram, manda /semestre pra saber quando o semestre vai dar a folguinha."
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)

def semestre(update, context):
    hoje = today('America/Sao_Paulo')
    aulas = datetime(2021, 7, 4)
    diff = aulas.diff(hoje).in_days()
    frases = [
        'Por favor, eu não aguento mais {} dias'
    ]
    frase = random.choice(frases)
    msg = frase.format(diff)
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)

def maquera(update, context):
    context.bot.forward_message(chat_id=update.effective_chat.id, from_chat_id='@becdbotfwd', message_id=2)



def send_welcome(update, context, new_member):
    welcome_message = """Bem-vinde, [@{}](tg://user?id={})!
    """.format(new_member.first_name, new_member.id)

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=welcome_message, parse_mode='Markdown')

def empty_message(update, context):
    """
        Handles empty messages:
            - User enters the group
            - User leaves the group
    """
    if update.message.new_chat_members:
        for new_member in update.message.new_chat_members:
            # Bot added to group
            if new_member.username != 'becdbot':
                return send_welcome(update, context, new_member)

if __name__ == '__main__':

    import os
    import argparse

    appname = 'becdbot'
    parser = argparse.ArgumentParser(description='BECD Bot')
    parser.add_argument('--local',
                        dest='is_local',
                        action='store_const',
                        const=True,
                        default=False,
                        help='Local run')
    args = parser.parse_args()
    BOT_API_TOKEN = os.getenv('BOT_API_TOKEN')
    
    updater = Updater(token=BOT_API_TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('aulas', aulas))
    dp.add_handler(CommandHandler('maquera', maquera))
    dp.add_handler(CommandHandler('fwd', fwd))
    dp.add_handler(CommandHandler('semestre', semestre))
    dp.add_handler(MessageHandler(Filters.status_update, empty_message))
    
    
    if not args.is_local:
        PORT = os.getenv('PORT')

        updater.start_webhook(listen="0.0.0.0",
                                port=int(PORT),
                                url_path=BOT_API_TOKEN,
                                webhook_url="https://"+ appname + ".herokuapp.com/" + BOT_API_TOKEN)
    else:
        updater.start_polling()

    updater.idle()

from telegram.ext import Updater, InlineQueryHandler, CommandHandler, MessageHandler, Filters

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Bot do BECD")

def send_welcome(update, context, new_member):
    welcome_message = """Bem-vindeee, @{}!
Se apresenta pra gente, é bixo ou veterano? 
Arroz em baixo ou em cima do feijão?
    """.format(new_member.username)

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=welcome_message)

def empty_message(update, context):
    """
        Handles empty messages:
            - User enters the group
            - User leaves the group
    """
    if update.message.new_chat_members:
        for new_member in update.message.new_chat_members:
            # Bot added to group
            if new_member.username == 'icmc-lgbt-welcome-bot':
                pass
            else:
                return send_welcome(update, context, new_member)

if __name__ == '__main__':

    import os
    import argparse

    parser = argparse.ArgumentParser(description='BECD Bot')
    parser.add_argument('--local',
                        dest='is_local',
                        action='store_const',
                        const=True,
                        default=False,
                        help='Local run')
    args = parser.parse_args()

    if not args.is_local:
        BOT_API_TOKEN = os.getenv('BOT_API_TOKEN')
    else:
        pass

    updater = Updater(token=BOT_API_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.status_update, empty_message))

    if not args.is_local:
        PORT = os.getenv('PORT')

        updater.start_webhook(listen="0.0.0.0",
                                port=int(PORT),
                                url_path=TOKEN,
                                webhook_url="https://"+ AppName + ".herokuapp.com/" + BOT_API_TOKEN)
    else:
        updater.start_polling()

    updater.idle()

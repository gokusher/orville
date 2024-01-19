import telebot
from message_handler import start
from database import TelegramUserDatabase

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
bot = telebot.TeleBot('6925542083:AAEr3D9LdQ6CxJIlqb4eU782JzIi7w0mel4')
db = TelegramUserDatabase()

@bot.message_handler(commands=['start'])
def start_handler(message):
    start(bot, message)

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    # Check if the callback is from the /start command
    if call.data == 'start':
        user_id = call.from_user.id
        user = db.get_user(user_id)

        if not user:
            db.add_user(call.from_user)
            bot.send_message(call.message.chat.id, f'Thank you, {call.from_user.first_name}, for pressing the Start button!')
        else:
            bot.send_message(call.message.chat.id, 'You have already pressed the Start button before.')

bot.polling(non_stop=True)


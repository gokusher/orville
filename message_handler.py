from database import TelegramUserDatabase

db = TelegramUserDatabase()

def start(bot, message):
    user_id = message.from_user.id
    user = db.get_user(user_id)

    if user:
        mess = f'Welcome back, {user["first_name"]} {user["last_name"]}!'
    else:
        db.add_user(message.from_user)
        mess = f'Hey, {message.from_user.first_name}! Welcome to the bot!'

    bot.send_message(message.chat.id, mess, parse_mode='html')


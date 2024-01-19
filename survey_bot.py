import telebot
from telebot import types


bot = telebot.TeleBot('6925542083:AAEr3D9LdQ6CxJIlqb4eU782JzIi7w0mel4')


user_responses = {}


questions = [
    "What is your favorite programming language?",
    "How often do you code each week?",
    "Would you recommend coding as a career to others?"
]


answers = [
    ["Python", "JavaScript", "Java", "Other"],
    ["Less than 5 hours", "5-10 hours", "More than 10 hours"],
    ["Yes", "No", "Maybe"]
]

@bot.message_handler(commands=['start'])
def start_survey(message):
    user_id = message.from_user.id
    user_responses[user_id] = []

    send_question(message.chat.id, user_id, 0)

def send_question(chat_id, user_id, question_number):
    if question_number < len(questions):
        question = questions[question_number]
        options = answers[question_number]

        markup = create_markup(options)
        bot.send_message(chat_id, f"{question}", reply_markup=markup)
    else:
        finish_survey(chat_id, user_id)

def create_markup(options):
    markup = types.InlineKeyboardMarkup(row_width=1)

    for option in options:
        button = types.InlineKeyboardButton(text=option, callback_data=option)
        markup.add(button)

    return markup

@bot.callback_query_handler(func=lambda call: True)
def handle_response(call):
    user_id = call.from_user.id

    if user_id in user_responses:
        user_responses[user_id].append(call.data)
        next_question = len(user_responses[user_id])

        if next_question < len(questions):
            send_question(call.message.chat.id, user_id, next_question)
        else:
            finish_survey(call.message.chat.id, user_id)


def finish_survey(chat_id, user_id):
    responses = "\n".join([f"Question {i+1}: {response}" for i, response in enumerate(user_responses[user_id])])

    bot.send_message(chat_id, "Survey completed! Here are your responses:\n" + responses)
    del user_responses[user_id]

if __name__ == "__main__":
    bot.polling(non_stop=True)

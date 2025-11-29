from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from database.base import engine, Base, get_db
from database.models import UserModel, TaskModel
from telebot import TeleBot, apihelper, telebot
import re


apihelper.ENABLE_MIDDLEWARE = True
Base.metadata.create_all(bind=engine)


apihelper.proxy = {
    "https":"socks5h://127.0.0.1:10810"
}


bot = telebot.TeleBot("8541091530:AAFcjlrZeH9Myl1Y8enCGcT-tRW8Hvz5NlY")

@bot.message_handler(commands=["start"])
def start(message):

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    btn_register = KeyboardButton("Register")
    btn_add = KeyboardButton("Add Task")
    btn_list = KeyboardButton("My Tasks")
    btn_Delete = KeyboardButton("Delete Task")
    btn_about = KeyboardButton("About Us")
    btn_contact = KeyboardButton("Contact Us")


    keyboard.row(btn_register)
    keyboard.row(btn_add, btn_list, btn_Delete)
    keyboard.row(btn_about, btn_contact)


    bot.send_message(
        message.chat.id,
        "Hello and Welcome to the Task Manager Telegram Bot\nSelect an Option:",
        reply_markup=keyboard
    )


@bot.message_handler(func=lambda m: m.text == "Register")
def start_register(message):
    db = next(get_db())
    telegram_id = message.from_user.id

    existing_user = db.query(UserModel).filter_by(telegram_id=telegram_id)
    if existing_user:
        bot.reply_to(message, "You are already registered.")
        return 
    
    bot.send_message(message.chat.id, "Please enter Your full name")
    bot.register_next_step_handler(message, ask_full_name)



def ask_full_name(message):
    full_name = message.text.strip()

    if not full_name or len(full_name) < 5:
        bot.send_message(message.chat.id, "Full name is not valid. Please enter again:")
        bot.register_next_step_handler(message, ask_full_name)
        return 
    
    bot.user_data = bot.user_data if hasattr(bot, "user_data") else {}
    bot.user_data[message.chat.id] = {"full_name":full_name}

    bot.send_message(message.chat.id, "Now please enter your email:")
    bot.register_next_step_handler(message, ask_email)


def ask_email(message):
    email = message.text.strip()

    if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
        bot.send_message(message.chat.id, "Invalid email format. Please enter again:")
        bot.register_next_step_handler(message, ask_email)
        return 
    
    data = bot.user_data.get(message.chat.id, {})
    full_name = data.get("full_name")

    if not full_name:
        bot.send_message(message.chat.id, "Error: full name missing. Please start again.")
        return

    db = next(get_db())

    existing_email = db.query(UserModel).filter_by(email=email).first()
    if existing_email:
        bot.send_message(message.chat.id, "This email is already registered. Try another:") 
        bot.register_next_step_handler(message, ask_email)
        return 
    
    telegram_id = message.from_user.id
    existing_user = db.query(UserModel).filter_by(telegram_id=telegram_id).first()
    if existing_user:
        bot.send_message(message.chat.id, "You are already registered.")
        return 
    
    new_user = UserModel(
        full_name=full_name,
        email=email,
        telegram_id=telegram_id
    )

    db.add(new_user)
    db.commit()
    bot.send_message(message.chat.id, "Registration completed successfully. Welcome!")

bot.infinity_polling()
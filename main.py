import os 
from dotenv import load_dotenv 
import telebot 
load_dotenv() 
TOKEN = os.getenv("TOKEN") 
if not TOKEN: 
 raise RuntimeError("  .env =5F TOKEN") 
bot = telebot.TeleBot(TOKEN)
@bot.message_handler(commands=['start']) 
def start(message): 
 bot.reply_to(message, "Welcome to our bot,for help write /help") 
@bot.message_handler(commands=['help']) 
def help_cmd(message): 
 bot.reply_to(message, "for Help write here please @bahara_2525")
@bot.message_handler(commands=['about']) 
def abouttg(message): 
 bot.reply_to(message, " My name is Bahara! ")
if __name__ == "__main__": 
 bot.infinity_polling(skip_pending=True)

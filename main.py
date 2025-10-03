
import os
from dotenv import load_dotenv
from telebot import types
from typing import List
import telebot

load_dotenv()
TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise RuntimeError("Токен не найден в .env файле")
bot = telebot.TeleBot(TOKEN)


def parse_ints_from_text(text: str) -> List[int]:
    """Выделяет из текста целые числа: нормализует запятые, игнорирует токены-команды."""
    text = text.replace(",", " ")
    tokens = [tok for tok in text.split() if not tok.startswith("/")]
    return [int(tok) for tok in tokens if is_int_token(tok)]


def is_int_token(t: str) -> bool:
    """Проверка токена на целое число (с поддержкой знака минус)."""
    if not t:
        return False
    t = t.strip()
    if t in {"-", ""}:
        return False
    return t.lstrip("-").isdigit()

@bot.message_handler(commands=['hide'])
def hide_kb(m):
 rm = types.ReplyKeyboardRemove()
 bot.send_message(m.chat.id, "спрятал клавиатуру", reply_markup=rm)
 
 
@bot.message_handler(commands=['confirm'])
def confirm_cmd(m):
    kb = types.InlineKeyboardMarkup()
    kb.add(
        types.InlineKeyboardButton("Yes", callback_data="confirm:yes"),
        types.InlineKeyboardButton("No", callback_data="confirm:no"),
        types.InlineKeyboardButton("Cancel", callback_data="confirm:cancel")  # новый пункт
    )
    bot.send_message(m.chat.id, "Подтвердить действие?", reply_markup=kb)


@bot.callback_query_handler(func=lambda c: c.data.startswith("confirm"))
def on_confirm(c):
    choice = c.data.split(":", 1)[1]

    bot.answer_callback_query(c.id, "Принято")
    bot.edit_message_reply_markup(c.message.chat.id, c.message.message_id, reply_markup=None)

    if choice == "yes":
        bot.send_message(c.message.chat.id, "Готово ✅")
    elif choice == "no":
        bot.send_message(c.message.chat.id, "Отменено ❌")
    elif choice == "cancel":
        bot.send_message(c.message.chat.id, "Действие отменено пользователем ⏹")

   

@bot.message_handler(commands=['start'])
def start(message):
    print(f"[PING] Пользователь {message.from_user.username} ({message.chat.id}) вызвал /start")
    print(f"[PING] Пользователь {message.from_user.username} ({message.chat.id}) вызвал /start")
    bot.reply_to(message, "Добро пожаловать! Используйте /help для справки")


@bot.message_handler(commands=['help'])
def help_cmd(message):
    print(f"[PING] Пользователь {message.from_user.username} ({message.chat.id}) вызвал /help")
    bot.reply_to(message, "/start - начать работу\n/help - помощь\n/about - информация о боте\n/sum - сумма чисел\n/hello - приветствие")


def make_main_kb() -> types.ReplyKeyboardMarkup:
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("O боте", "Сумма")
    kb.row("/hello")
    kb.row("/about", "/sum")
    kb.row("/hide", "/show")
    return kb

@bot.message_handler(commands=['show'])
def show_kb(m):
   bot.send_message(m.chat.id, "Показал клавиатуру.", reply_markup=make_main_kb())

@bot.message_handler(commands=['hello'])
def hello(message):
    bot.reply_to(message, "Привет! Я твой бот 😊", reply_markup=make_main_kb())


@bot.message_handler(commands=['about'])
def about(message):
    print(f"[PING] Пользователь {message.from_user.username} ({message.chat.id}) вызвал /about")
    bot.reply_to(
        message,
        "🤖 Бот: tg-bot-simple\n"
        "Автор: Bahara Abdullahi\n"
        "Версия: 1.0\n"
        "Назначение: учебный проект"
    )


@bot.message_handler(commands=['ping'])
def ping(message):
    print(f"[PING] Пользователь {message.from_user.username} ({message.chat.id}) вызвал /ping")
    bot.reply_to(message, "pong 🏓")


@bot.message_handler(commands=['sum'])
def cmd_sum(message):
    parts = message.text.split()
    numbers = []

    for p in parts[1:]:
        if p.isdigit():
            numbers.append(int(p))

    if not numbers:
        bot.reply_to(message, "Напиши число: /sum 2 3 10")
    else:
        bot.reply_to(message, f"Сумма: {sum(numbers)}")
        
@bot.message_handler(commands=['max'])
def cmd_max(message):
    numbers = parse_ints_from_text(message.text)
    if not numbers:
        bot.reply_to(message, "Пример: /max 2 3 10")
    else:
        bot.reply_to(message, f"Максимум: {max(numbers)}")        
        
@bot.message_handler(commands=['weather'])
def weather_cmd(message):
 weather = fetch_weather_moscow_open_meteo()
 bot.reply_to(message, f"{weather}")

def fetch_weather_moscow_open_meteo() -> str:
 url = "https://api.open-meteo.com/v1/forecast"
 params = {
  "latitude": 55.7558,
  "longitude": 37.6173,
  "current": "temperature_2m",
  "timezone": "Europe/Moscow"
 }
 try:
  r = requests.get(url, params=params, timeout=5)
  r.raise_for_status()
  t = r.json()["current"]["temperature_2m"]
  return f"Москва: сейчас {round(t)}°C"
 except Exception:
  return "Не удалось получить погоду."


@bot.message_handler(func=lambda m: m.text == "О боте")  # Исправлена опечатка
def kb_about(m):
    bot.reply_to(m, "Я учебный бот. Доступные команды: /start, /help, /about, /sum, /hello")


@bot.message_handler(func=lambda m: m.text == "Сумма")
def kb_sum(m: types.Message) -> None:
    bot.send_message(m.chat.id, "Введите числа через пробел или запятую:")
    bot.register_next_step_handler(m, on_sum_numbers)


def on_sum_numbers(m: types.Message) -> None:
    nums = parse_ints_from_text(m.text)
    
    if not nums:
        bot.reply_to(m, "Не вижу чисел. Пример: 2 3 10")
    else:
        bot.reply_to(m, f"Сумма: {sum(nums)}")


if __name__ == "__main__":
    print("Бот запущен...")
    bot.infinity_polling(skip_pending=True)
    
    
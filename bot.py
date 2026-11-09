import time
import telebot
from telebot import types

TOKEN = "9071693829:AAHa0vTKjKAdLDNh_qobthiWXAFaae6n8t8"
CHANNEL_USERNAME = "@UzbekHamkorlar"

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
  user_name = message.from_user.first_name
  user_id = message.from_user.id

  try:
    chat_member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
    if chat_member.status in ['member', 'administrator', 'creator']:
      bot.send_message(
          message.chat.id,
          f"Assalomu alaykum, {user_name}! 🤝\n\n'Hamkor Bot'ga xush kelibsiz."
          " Siz allaqachon kanalimizga a'zosiz, xizmatlardan foydalanishingiz"
          " mumkin!",
      )
      return
  except Exception as e:
    print(f"Xatolik: {e}")

  markup = types.InlineKeyboardMarkup()
  channel_btn = types.InlineKeyboardButton(
      "📢 Kanalimizga obuna bo'lish", url=f"https://t.me/{CHANNEL_USERNAME[1:]}"
  )
  check_btn = types.InlineKeyboardButton(
      "✅ Obunani tekshirish", callback_data="check_sub"
  )
  markup.add(channel_btn)
  markup.add(check_btn)

  bot.send_message(
      message.chat.id,
      f"Assalomu alaykum, {user_name}! 🤝\n\n'Hamkor Bot'dan foydalanish uchun"
      f" avval quyidagi {CHANNEL_USERNAME} kanalimizga a'zo bo'ling:",
      reply_markup=markup,
  )


@bot.callback_query_handler(func=lambda call: call.data == 'check_sub')
def callback_inline(call):
  user_id = call.from_user.id
  try:
    chat_member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
    if chat_member.status in ['member', 'administrator', 'creator']:
      bot.answer_callback_query(call.id, "Rahmat! Obuna tasdiqlandi ✅")
      bot.send_message(
          call.message.chat.id,
          "🎉 Tabriklayman! Obunangiz tasdiqlandi. Endi 'Hamkor Bot'"
          " xizmatlaridan to'liq foydalanishingiz mumkin.",
      )
    else:
      bot.answer_callback_query(
          call.id,
          "❌ Siz hali kanalga obuna bo'lmadingiz!",
          show_alert=True,
      )
  except Exception as e:
    bot.answer_callback_query(
        call.id, "Xatolik yuz berdi, keyinroq urinib ko'ring.", show_alert=True
    )


print('Hamkor Bot majburiy obuna funksiyasi bilan ishga tushdi...')

while True:
  try:
    bot.infinity_polling(timeout=60, long_polling_timeout=60)
  except Exception as e:
    print(f"Aloqa uzildi, qayta ulanmoqda... Xato: {e}")
    time.sleep(5)
    

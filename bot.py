import telebot
from telebot import types

# Tokeningiz
TOKEN = "9071693829:AAGOFQmXUl_zKCQOUZ01M3HYbxrH86Gxq2I"
bot = telebot.TeleBot(TOKEN)

# Vaqtinchalik baza (foydalanuvchilar, balans va referallar uchun)
users_db = {} 
# users_db[user_id] = {"balance": 0, "referrals": 0, "phone": ""}

# Homiy kanal (Majburiy obuna uchun - o'z kanalingiz username'ini yozing)
CHANNEL_USERNAME = "@uz_hamkor_bot"

# 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 - Funksiyalar jamlanmasi

# 1. Start va Asosiy Menyu funksiyasi
@bot.message_handler(commands=['start'])
def start_command(message):
    user_id = message.from_id
    args = message.text.split()
    
    # Referal tizimini hisoblash (2-funksiya: Referal orqali kirish)
    if len(args) > 1:
        ref_id = args[1]
        if ref_id.isdigit() and int(ref_id) != user_id:
            if user_id not in users_db and int(ref_id) in users_db:
                users_db[int(ref_id)]["referrals"] += 1
                users_db[int(ref_id)]["balance"] += 1000 # Har bir taklif uchun 1000 so'm
                try:
                    bot.send_message(int(ref_id), "🎉 Yangi do'stingiz havolangiz orqali qo'shildi! Balansingizga 1000 so'm qo'shildi.")
                except:
                    pass

    # Yangi foydalanuvchini bazaga qo'shish
    if user_id not in users_db:
        users_db[user_id] = {"balance": 0, "referrals": 0, "phone": "Kiritilmagan"}

    # 3-funksiya: Majburiy obunani tekshirish
    try:
        chat_member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        if chat_member.status in ['left', 'kicked']:
            send_subscribe_channel(message)
            return
    except:
        pass # Kanal topilmasa yoki xatolik bo'lsa o'tkazib yuboradi

    # Asosiy menyuni chiqarish
    show_main_menu(message.chat.id)

def send_subscribe_channel(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📢 Kanalga obuna bo'lish", url=f"https://t.me/{CHANNEL_USERNAME.replace('@','')}"))
    markup.add(types.InlineKeyboardButton("✅ Obunani tekshirish", callback_data="check_sub"))
    bot.send_message(message.chat.id, "⚠️ Botdan foydalanish uchun quyidagi kanalimizga obuna bo'ling:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def callback_check_sub(call):
    user_id = call.from_user.id
    try:
        chat_member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        if chat_member.status not in ['left', 'kicked']:
            bot.answer_callback_query(call.id, "Rahmat! Obunangiz tasdiqlandi ✅")
            bot.delete_message(call.message.chat.id, call.message.message_id)
            show_main_menu(call.message.chat.id)
        else:
            bot.answer_callback_query(call.id, "❌ Siz hali kanalga obuna bo'lmadingiz!", show_alert=True)
    except:
        show_main_menu(call.message.chat.id)

def show_main_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(types.KeyboardButton("💰 Balansim"), types.KeyboardButton("🔗 Referal havola"))
    markup.add(types.KeyboardButton("💸 Pul chiqarish"), types.KeyboardButton("ℹ️ Ma'lumot"))
    markup.add(types.KeyboardButton("☎️ Aloqa / Admin"))
    bot.send_message(chat_id, "Asosiy menyushga xush kelibsiz! Kerakli bo'limni tanlang:", reply_markup=markup)

# Xabarlar routeri (Barcha tugmalar va matnlar uchun)
@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    user_id = message.from_id
    text = message.text

    if user_id not in users_db:
        users_db[user_id] = {"balance": 0, "referrals": 0, "phone": "Kiritilmagan"}

    # 4-funksiya: Balansni tekshirish
    if text == "💰 Balansim":
        bal = users_db[user_id]["balance"]
        refs = users_db[user_id]["referrals"]
        bot.reply_to(message, f"👤 Profilingiz:\n\n💵 Balansingiz: {bal} so'm\n👥 Taklif qilgan do'stlaringiz: {refs} ta")

    # 5-funksiya: Shaxsiy referal havolani olish
    elif text == "🔗 Referal havola":
        bot_info = bot.get_me()
        ref_link = f"https://t.me/{bot_info.username}?start={user_id}"
        bot.reply_to(message, f"🔗 Sizning taklif havolangiz:\n\n{ref_link}\n\nDo'stlaringizni shu havola orqali taklif qiling va har biriga pul oling!")

    # 6-funksiya: Pul chiqarish uchun ariza berish
    elif text == "💸 Pul chiqarish":
        bal = users_db[user_id]["balance"]
        if bal < 10000:
            bot.reply_to(message, f"❌ Pul chiqarish uchun minimal miqdor: 10,000 so'm.\nSizning balansingiz: {bal} so'm.")
        else:
            bot.reply_to(message, "💳 Karta raqamingizni yuboring (masalan: 8600... yoki Click raqam):")
            bot.register_next_step_handler(message, process_withdraw)

    # 7-funksiya: Bot haqida ma'lumot
    elif text == "ℹ️ Ma'lumot":
        bot.reply_to(message, "ℹ️ Bu bot do'stlaringizni taklif qilish orqali pul ishlash va xizmatlardan foydalanish uchun mo'ljallangan hamkorlik platformasi.")

    # 8-funksiya: Aloqa / Admin bilan bog'lanish
    elif text == "☎️ Aloqa / Admin":
        bot.reply_to(message, "📞 Savollar bo'yicha murojaat qiling: @Admin_Username")

    # 9-funksiya: Admin maxfiy paneli (Faqat admin uchun)
    elif text.startswith("/admin"):
        if user_id == 7777777: # O'z Telegram ID raqamingizni yozib qo'ying
            total_users = len(users_db)
            bot.reply_to(message, f"👑 Admin panel:\n\nJami foydalanuvchilar: {total_users} ta")
        else:
            bot.reply_to(message, "Sizda admin huquqi yo'q.")
            
    else:
        bot.reply_to(message, "Iltimos, pastdagi tugmalardan foydalaning 👇")

# 10-funksiya: Pul yechish jarayonini yakunlash
def process_withdraw(message):
    user_id = message.from_id
    card_info = message.text
    bal = users_db[user_id]["balance"]
    
    if bal >= 10000:
        users_db[user_id]["balance"] = 0 # Balansni nolga tushirish
        bot.reply_to(message, f"✅ Pul chiqarish uchun ariza qabul qilindi!\nKarta: {card_info}\nMiqdor: {bal} so'm.\nTez orada ko'rib chiqiladi.")
    else:
        bot.reply_to(message, "❌ Xatolik yuz berdi. Balans yetarli emas.")

if __name__ == "__main__":
    print("Hamkor Bot 10 ta funksiya bilan to'liq ishga tushdi...")
    bot.infinity_polling(timeout=60, long_polling_timeout=60)
                  

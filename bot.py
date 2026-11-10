import telebot
from telebot import types
import random

TOKEN = "9071693829:AAECdwtvKxYz9HEj5hAnI4s8togFB1qJD6M"
bot = telebot.TeleBot(TOKEN)

users_db = {}
CHANNEL_USERNAME = "@uz_hamkor_bot"

@bot.message_handler(commands=['start'])
def start_command(message):
    user_id = message.from_user.id
    args = message.text.split()
    
    if len(args) > 1:
        ref_id = args[1]
        if ref_id.isdigit() and int(ref_id) != user_id:
            if user_id not in users_db and int(ref_id) in users_db:
                users_db[int(ref_id)]["referrals"] += 1
                users_db[int(ref_id)]["balance"] += 1000
                try:
                    bot.send_message(int(ref_id), "Yangi do'stingiz havolangiz orqali qo'shildi! Balansingizga 1000 so'm qo'shildi.")
                except:
                    pass

    if user_id not in users_db:
        users_db[user_id] = {"balance": 0, "referrals": 0, "bonus_taken": False}

    try:
        chat_member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        if chat_member.status in ['left', 'kicked']:
            send_subscribe_channel(message)
            return
    except:
        pass

    show_main_menu(message.chat.id)

def send_subscribe_channel(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Kanalga obuna bo'lish", url=f"https://t.me/{CHANNEL_USERNAME.replace('@','')}"))
    markup.add(types.InlineKeyboardButton("Obunani tekshirish", callback_data="check_sub"))
    bot.send_message(message.chat.id, "Botdan foydalanish uchun quyidagi kanalimizga obuna bo'ling:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def callback_check_sub(call):
    user_id = call.from_user.id
    try:
        chat_member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        if chat_member.status not in ['left', 'kicked']:
            bot.answer_callback_query(call.id, "Rahmat! Obunangiz tasdiqlandi")
            bot.delete_message(call.message.chat.id, call.message.message_id)
            show_main_menu(call.message.chat.id)
        else:
            bot.answer_callback_query(call.id, "Siz hali kanalga obuna bo'lmadingiz!", show_alert=True)
    except:
        show_main_menu(call.message.chat.id)

def show_main_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(types.KeyboardButton("💰 Balansim"), types.KeyboardButton("🔗 Referal havola"))
    markup.add(types.KeyboardButton("🎁 Kunlik bonus"), types.KeyboardButton("💸 Pul chiqarish"))
    markup.add(types.KeyboardButton("🤖 AI Video G'oyalari"), types.KeyboardButton("🚀 Pullik Xizmatlar & Reklama"))
    markup.add(types.KeyboardButton("🎮 Mini O'yinlar"), types.KeyboardButton("💱 Valyuta kurslari"))
    markup.add(types.KeyboardButton("📊 Statistika"), types.KeyboardButton("ℹ️ Ma'lumot"))
    bot.send_message(chat_id, "Asosiy menyuga xush kelibsiz! Quyidagi 20 ta imkoniyatdan birini tanlang:", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    user_id = message.from_user.id
    text = message.text

    if user_id not in users_db:
        users_db[user_id] = {"balance": 0, "referrals": 0, "bonus_taken": False}

    # 1. Balansim
    if text == "💰 Balansim":
        bal = users_db[user_id]["balance"]
        refs = users_db[user_id]["referrals"]
        bot.reply_to(message, f"👤 Profilingiz:\n\n1️⃣ Balansingiz: {bal} so'm\n2️⃣ Takliflar: {refs} ta\n3️⃣ Status: Faol foydalanuvchi")

    # 2. Referal havola
    elif text == "🔗 Referal havola":
        bot_info = bot.get_me()
        ref_link = f"https://t.me/{bot_info.username}?start={user_id}"
        bot.reply_to(message, f"🔗 Taklif havolangiz:\n\n{ref_link}\n\n4️⃣ Har bir do'st uchun: +1000 so'\n5️⃣ Do'stlar almashinuvi faol.")

    # 3. Kunlik bonus
    elif text == "🎁 Kunlik bonus":
        if not users_db[user_id]["bonus_taken"]:
            users_db[user_id]["balance"] += 500
            users_db[user_id]["bonus_taken"] = True
            bot.reply_to(message, "🎁 Tabriklaymiz! 6️⃣ Kunlik bonus sifatida balansingizga 500 so'm qo'shildi.")
        else:
            bot.reply_to(message, "❌ Siz bugungi 7️⃣ kunlik bonusni allaqachon olgansiz! Ertaga yana urinib ko'ring.")

    # 4. Pul chiqarish
    elif text == "💸 Pul chiqarish":
        bal = users_db[user_id]["balance"]
        if bal < 10000:
            bot.reply_to(message, f"❌ 8️⃣ Minimal chiqarish miqdori: 10,000 so'm.\nJoriy balans: {bal} so'm.")
        else:
            bot.reply_to(message, "💳 9️⃣ Karta raqamingizni yuboring (8600... yoki Click):")
            bot.register_next_step_handler(message, process_withdraw)

    # 5. AI Video G'oyalari
    elif text == "🤖 AI Video G'oyalari":
        ai_text = (
            "🎬 AI Video Imkoniyatlari:\n\n"
            "🔟 Ssenariya: ChatGPT orqali tezkor matn\n"
            "1️⃣1️⃣ Ovoz: ElevenLabs orqali jonli ovoz\n"
            "1️⃣2️⃣ Montaj: CapCut/Canva yordamida tezkor yasash"
        )
        bot.reply_to(message, ai_text)

    # 6. Pullik Xizmatlar & Reklama
    elif text == "🚀 Pullik Xizmatlar & Reklama":
        paid_text = (
            "🚀 Pullik Xizmatlar:\n\n"
            "1️⃣3️⃣ Kanalda reklama joylash\n"
            "1️⃣4️⃣ Premium AI video tayyorlab berish\n"
            "1️⃣5️⃣ Bot ochish va sozlash xizmati\n\n"
            "Murojaat uchun: @Admin_Username"
        )
        bot.reply_to(message, paid_text)

    # 7. Mini O'yinlar
    elif text == "🎮 Mini O'yinlar":
        rand_num = random.randint(1, 10)
        bot.reply_to(message, f"🎮 Mini o'yin bo'limi:\n\n1️⃣6️⃣ Omadli raqam: {rand_num}\n1️⃣7️⃣ Tez kunda yangi o'yinlar qo'shiladi!")

    # 8. Valyuta kurslari
    elif text == "💱 Valyuta kurslari":
        bot.reply_to(message, "💱 Markaziy bank kurslari:\n\n1️⃣8️⃣ 1 USD = ~12,800 so'm\n1️⃣9️⃣ 1 EUR = ~13,500 so'm")

    # 9. Statistika
    elif text == "📊 Statistika":
        total_users = len(users_db)
        bot.reply_to(message, f"📊 Bot statistikasi:\n\n2️⃣0️⃣ Jami ro'yxatdan o'tganlar: {total_users} ta foydalanuvchi")

    # 10. Ma'lumot
    elif text == "ℹ️ Ma'lumot":
        bot.reply_to(message, "ℹ️ Bu bot sizga ham daromad topish, ham sun'iy intellekt va pullik xizmatlardan foydalanish imkonini beradi.")

    elif text.startswith("/admin"):
        total_users = len(users_db)
        bot.reply_to(message, f"👑 Admin panel:\nJami foydalanuvchilar: {total_users} ta")
            
    else:
        bot.reply_to(message, "Iltimos, pastdagi tugmalardan foydalaning.")

def process_withdraw(message):
    user_id = message.from_user.id
    card_info = message.text
    bal = users_db[user_id]["balance"]
    
    if bal >= 10000:
        users_db[user_id]["balance"] = 0
        bot.reply_to(message, f"✅ Pul chiqarish uchun ariza qabul qilindi!\nKarta: {card_info}\nMiqdor: {bal} so'm.")
    else:
        bot.reply_to(message, "❌ Xatolik yuz berdi. Balans yetarli emas.")

if __name__ == "__main__":
    print("Bot 20 ta imkoniyat bilan ishga tushdi...")
    bot.infinity_polling(timeout=60, long_polling_timeout=60)

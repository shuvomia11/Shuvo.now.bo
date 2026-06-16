import telebot
from telebot import types, apihelper
import requests
import time
import threading
import random

# কনফিগারেশন
API_KEY = "MUBTR1MKUBO"
BOT_TOKEN = "8510677584:AAG-y26-o5m7hUit-mVA1OHAKgLtcTHaxbI"
BASE_URL = "https://api.2oo9.cloud/MXS47FLFX0U/tness/@public/api"
HEADERS = {"mauthapi": API_KEY}
ADMIN_ID = "6136815573"
GROUP_URL = "https://t.me/tem_withh"

bot = telebot.TeleBot(BOT_TOKEN)

user_ranges = {}
user_numbers = {}
user_countries = {}

def clean_number(num):
    return "".join(filter(str.isdigit, str(num)))

def get_flag(country_name):
    flags = {
        "Bangladesh": "🇧🇩", "India": "🇮🇳", "USA": "🇺🇸", 
        "UK": "🇬🇧", "Pakistan": "🇵🇰", "Russia": "🇷🇺",
        "Indonesia": "🇮🇩", "Malaysia": "🇲🇾", "China": "🇨🇳",
        "Guinea": "🇲🇱", "Tanzania": "🇹🇿"
    }
    return flags.get(country_name, "🌍")

def auto_check_otp(chat_id, phone_number, country):
    for _ in range(60): 
        try:
            response = requests.get(f"{BASE_URL}/success-otp", headers=HEADERS, timeout=10)
            data = response.json()
            if data.get("meta", {}).get("code") == 200:
                for item in data.get("data", {}).get("otps", []):
                    if clean_number(item.get("number")) in clean_number(phone_number):
                        otp = "".join(filter(str.isdigit, item.get("message", "")))[-6:]
                        msg_text = (f"✅ 𝙾𝚃𝙿 𝚁𝙴𝙲𝙴𝙸𝚅𝙴𝙳\n\n🟢 𝙲𝚘𝚞𝚗𝚝𝚛𝚢 : {get_flag(country)} {country}\n📞 𝙽𝚞𝚖𝚋𝚎𝚛 : +{phone_number}\n\n🔑 𝙾𝚃𝙿 : `{otp}`")
                        kb = types.InlineKeyboardMarkup()
                        kb.add(types.InlineKeyboardButton(text=f"{otp}", copy_text=types.CopyTextButton(text=otp)))
                        bot.send_message(chat_id, msg_text, parse_mode="Markdown", reply_markup=kb)
                        return
        except: pass
        time.sleep(2)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add(types.KeyboardButton("📱 𝙽𝚄𝙼𝙱𝙴𝚁"), types.KeyboardButton("🔐 𝙶𝙴𝚃 2𝙵𝙰 𝙲𝙾𝙳𝙴"), types.KeyboardButton("👑 𝙰𝙳𝙼𝙸𝙽 𝚂𝚄𝙿𝙿𝙾𝚁𝚃"))
    welcome_text = "👋𓆩𓆩𝚆𝙴𝙻𝙲𝙾𝙼𝙴 𝚃𝙾 𝙾𝚃𝙿 𝚂𝙴𝚁𝚅𝙸𝙲𝙴𓆪𓆪\n\n🤖 𝚃𝙴𝙰𝙼 𝚆𝙸𝚃𝙷 3.0 𝙽𝚄𝙼𝙱𝙴𝚁 𝙱𝙾𝚃"
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    if message.text == "📱 𝙽𝚄𝙼𝙱𝙴𝚁":
        msg = bot.send_message(message.chat.id, "⚙️ 𝙿𝙻𝙴𝙰𝚂𝙴 𝙴𝙽𝚃𝙴𝚁 𝚈𝙾𝚄𝚁 𝚁𝙰𝙽𝙶𝙴\n\n🔢 𝙴𝚡𝚊𝚖𝚙𝚕𝚎 : `2245564`", parse_mode="Markdown")
        bot.register_next_step_handler(msg, process_number)
    elif message.text == "🔐 𝙶𝙴𝚃 2𝙵𝙰 𝙲𝙾𝙳𝙴":
        msg = bot.send_message(message.chat.id, "🔐 𝙿𝙻𝙴𝙰𝚂𝙴 𝙴𝙽𝚃𝙴𝚁 𝚈𝙾𝚄𝚁 𝟸𝙵𝙰 𝙺𝙴𝚈")
        bot.register_next_step_handler(msg, process_2fa)
    elif message.text == "👑 𝙰𝙳𝙼𝙸𝙽 𝚂𝚄𝙿𝙿𝙾𝚁𝚃":
        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton("📩 এডমিনকে মেসেজ দিন", url=f"tg://user?id={ADMIN_ID}"))
        bot.send_message(message.chat.id, "💬 যেকোনো সমস্যার জন্য এডমিনকে মেসেজ দিন।", reply_markup=kb)

def process_2fa(message):
    code = str(random.randint(100000, 999999))
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text=f"{code}", copy_text=types.CopyTextButton(text=code)))
    bot.send_message(message.chat.id, f"🔐 𝚈𝙾𝚄𝚁 𝟸𝙵𝙰 𝙲𝙾𝙳𝙴 ✅\n\n`{code}`", parse_mode="Markdown", reply_markup=kb)

def process_number(message, edit_msg=None):
    rid = message.text if not edit_msg else user_ranges.get(message.chat.id)
    if not edit_msg: user_ranges[message.chat.id] = rid
    
    if edit_msg:
        bot.edit_message_text("⏳ 𝙿𝙻𝙴𝙰𝚂𝙴 𝚆𝙰𝙸𝚃...\n🔄 𝙽𝚄𝙼𝙱𝙴𝚁 𝙶𝙴𝙽𝙴𝚁𝙰𝚃𝙸𝙽𝙶...", message.chat.id, edit_msg.message_id)
    else:
        edit_msg = bot.send_message(message.chat.id, "⏳ 𝙿𝙻𝙴𝙰𝚂𝙴 𝚆𝙰𝙸𝚃...\n🔄 𝙽𝚄𝙼𝙱𝙴𝚁 𝙶𝙴𝙽𝙴𝚁𝙰𝚃𝙸𝙽𝙶...")

    try:
        response = requests.post(f"{BASE_URL}/getnum", json={"rid": rid}, headers=HEADERS, timeout=15)
        data = response.json()
        if data.get("meta", {}).get("code") == 200:
            full_num = str(data.get("data", {}).get('full_number')).replace("+", "")
            country = data.get("data", {}).get('country', 'Unknown')
            user_numbers[message.chat.id] = full_num
            user_countries[message.chat.id] = country
            
            msg = (f"✅ 𝙽𝚞𝚖𝚋𝚎𝚛 𝙰𝚜𝚜𝚒𝚐𝚗𝚎𝚍 !\n\n🟢 𝙲𝚘𝚞𝚗𝚝𝚛𝚢 : {get_flag(country)} {country}\n📞 𝙽𝚞𝚖𝚋𝚎𝚛 : +{full_num}\n📦 𝚂𝚎𝚛𝚟𝚒𝚌𝚎 : 𝙵𝚊𝚌𝚎𝚋𝚘𝚘𝚔\n\n⏳ 𝚆𝙰𝙸𝚃𝙸𝙽𝙶 𝙵𝙾𝚁 𝙾𝚃𝙿...")
            kb = types.InlineKeyboardMarkup(row_width=1)
            kb.add(types.InlineKeyboardButton(text=f"+{full_num}", copy_text=types.CopyTextButton(text=f"+{full_num}")))
            kb.add(types.InlineKeyboardButton("🔄 𝙲𝚑𝚊𝚗𝚐𝚎 𝙽𝚞𝚖𝚋𝚎𝚛", callback_data="change_num"))
            kb.add(types.InlineKeyboardButton("🔍 𝙾𝚃𝙿 𝚂𝙴𝙰𝚁𝙲𝙷", callback_data="otp_search"))
            kb.add(types.InlineKeyboardButton("🔐 𝙾𝚃𝙿 𝙶𝚁𝙾𝚄𝙿", url=GROUP_URL))
            
            bot.edit_message_text(msg, message.chat.id, edit_msg.message_id, parse_mode="Markdown", reply_markup=kb)
            threading.Thread(target=auto_check_otp, args=(message.chat.id, full_num, country)).start()
        else:
            bot.edit_message_text("❌ নাম্বার পাওয়া যায়নি!", message.chat.id, edit_msg.message_id)
    except Exception as e:
        bot.edit_message_text(f"❌ ত্রুটি: {e}", message.chat.id, edit_msg.message_id)

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == "change_num":
        process_number(call.message, edit_msg=call.message)
    elif call.data == "otp_search":
        bot.answer_callback_query(call.id, "অপেক্ষা করুন...")
        user_num = user_numbers.get(call.message.chat.id)
        country = user_countries.get(call.message.chat.id, "Unknown")
        threading.Thread(target=auto_check_otp, args=(call.message.chat.id, user_num, country)).start()

# বট স্টার্ট করার সময় টাইমআউট বাড়িয়ে দেওয়া হয়েছে
print("Bot is running...")
bot.polling(none_stop=True, timeout=60, long_polling_timeout=60)

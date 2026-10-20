import telebot
from telebot import types

TOKEN = '8749141019:AAH-cte4bASOdtN4HrirRlv_Wy3Wl1gmtKo'

bot = telebot.TeleBot(TOKEN)

readers_list = []
listeners_list = []
apologized_list = []

HEADER_TEXT = """<b>السَّـلام عليكُـم و رحمةُ اللهِ و بركَاتُـه

🩵 حَـيَّـاڪنَّ اللّٰـه وَ بَيَّـاڪُنَّ طَـالِـبَـات قَنـاة 
                              عَلـى القُــرآنِ تَعَـاهَـدنَـــــــا 🩵

📖 •{ وَإِذَا قُرِئَ الْقُرْءَانُ فَاسْتَمِعُوا لَهُ وَأَنصِتُوا لَعَلَّكُمْ تُرْحَمُونَ }•

🌸 الحَلقَـــــة : تَصحِيـح تِــــــلاوة</b>

<blockquote><b>🗓️ قَـــــائِـمَــــــةُ الأدواࢪ :</b></blockquote>
"""

FOOTER_TEXT = """

---------------------------------------------

<b>طيَّـــــــــــــب اللّٰـه أنفَـاسَڪُـنَّ وَ أسمَـاعَڪُـنَّ 🌷
-٭
سُبْحَانَــكَ اللهـمَّ وَبِحَـمْــدِكَ نَـشْـهَـدُ أن لَّا إلـٰهَ إلَّا أنـتَ
 نَـسـتَـغـفِـرُكَ وَنَـتــوبُ إليْــك . 🌸</b>"""

def get_formatted_list():
    text = HEADER_TEXT + "\n<b>✏️ المُسجّــلاتُ لِلقِــࢪاءة ↓ ↓ :</b>\n"
    if not readers_list:
        text += "<i>(لا يوجد طالبات مسجلات حالياً)</i>\n"
    else:
        for i, item in enumerate(readers_list, 1):
            status = " ✅ <b>(قرأت)</b>" if item['done'] else ""
            user_mention = f"<a href='tg://user?id={item['id']}'>{item['name']}</a>"
            text += f"<b>{i}.</b> {user_mention}{status}\n"
            
    text += "\n<b>🎧 المُسْتَمِعَاتُ ↓ ↓ :</b>\n"
    if not listeners_list:
        text += "<i>(لا يوجد)</i>\n"
    else:
        for i, item in enumerate(listeners_list, 1):
            user_mention = f"<a href='tg://user?id={item['id']}'>{item['name']}</a>"
            text += f"<b>{i}.</b> {user_mention}\n"

    text += "\n<b>🍓 المُعْتَذِرَاتُ ↓ ↓ :</b>\n"
    if not apologized_list:
        text += "<i>(لا يوجد)</i>\n"
    else:
        for i, item in enumerate(apologized_list, 1):
            user_mention = f"<a href='tg://user?id={item['id']}'>{item['name']}</a>"
            text += f"<b>{i}.</b> {user_mention}\n"

    text += FOOTER_TEXT
    return text

def get_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn_join = types.InlineKeyboardButton("تَسجِيــل دور ✏️", callback_data="join_reader")
    btn_done = types.InlineKeyboardButton("قَـــرأت ✅", callback_data="mark_done")
    btn_listen = types.InlineKeyboardButton("المُستمِعَـــات 🎧", callback_data="join_listener")
    btn_apologize = types.InlineKeyboardButton("المُعتـــذرات 🍓", callback_data="join_apologize")
    markup.add(btn_join, btn_done, btn_listen, btn_apologize)
    return markup

# 1. أمر لبدء قائمة جديدة
@bot.message_handler(commands=['start', 'قائمة', 'start_list'])
def send_list(message):
    bot.send_message(message.chat.id, get_formatted_list(), parse_mode='HTML', reply_markup=get_keyboard())

# التفاعل مع الأزرار
@bot.callback_query_handler(func=lambda call: True)
def callback_buttons(call):
    user_id = call.from_user.id
    user_name = call.from_user.first_name
    global readers_list, listeners_list, apologized_list
    
    action = call.data
    
    if action == "join_reader":
        if not any(item['id'] == user_id for item in readers_list):
            listeners_list = [n for n in listeners_list if n['id'] != user_id]
            apologized_list = [n for n in apologized_list if n['id'] != user_id]
            readers_list.append({'id': user_id, 'name': user_name, 'done': False})
            bot.answer_callback_query(call.id, f"تم تسجيلك في دور القراءة يا {user_name} ✏️")
        else:
            bot.answer_callback_query(call.id, "أنتِ مسجلة بالفعل في قائمة القراءة!", show_alert=True)
            
    if action == "mark_done":
        found = False
        for item in readers_list:
            if item['id'] == user_id:
                item['done'] = True
                found = True
                break
        if found:
            bot.answer_callback_query(call.id, f"بَـارك اللّٰـه فيـكِ يَـا {user_name}, تمّ تثبيت إنجازك ✅")
        else:
            bot.answer_callback_query(call.id, "لسـتِ مُسجّلـة فـي قَـائمـة القـراءة الحاليّـة!", show_alert=True)
            
    if action == "join_listener":
        readers_list = [item for item in readers_list if item['id'] != user_id]
        apologized_list = [item for item in apologized_list if item['id'] != user_id]
        if not any(item['id'] == user_id for item in listeners_list):
            listeners_list.append({'id': user_id, 'name': user_name})
        bot.answer_callback_query(call.id, f"تم تسجيلك كمستمعة يا {user_name} 🎧")
        
    if action == "join_apologize":
        readers_list = [item for item in readers_list if item['id'] != user_id]
        listeners_list = [item for item in listeners_list if item['id'] != user_id]
        if not any(item['id'] == user_id for item in apologized_list):
            apologized_list.append({'id': user_id, 'name': user_name})
        bot.answer_callback_query(call.id, f"تم تسجيل اعتذارك يا {user_name} 🍓")

    try:
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=get_formatted_list(),
            parse_mode='HTML',
            reply_markup=get_keyboard()
        )
    except Exception:
        pass

# 2. أمر completion لإرسال القائمة المحدثة
@bot.message_handler(commands=['completion'])
def completion_list(message):
    bot.send_message(message.chat.id, get_formatted_list(), parse_mode='HTML', reply_markup=get_keyboard())

# 3. أمر next للنداء على الطالبة التالية
@bot.message_handler(commands=['next', 'التالي'])
def next_student(message):
    if readers_list:
        next_item = None
        for item in readers_list:
            if not item['done']:
                next_item = item
                break
        if next_item:
            user_mention = f"<a href='tg://user?id={next_item['id']}'>{next_item['name']}</a>"
            bot.send_message(message.chat.id, f"🔊 <b>الدّور الآن علـى الطّالبـة: {user_mention}</b>\n\nتفضّلـي للقِـراءة بَـارك اللَّـه فيـكِ 🌹", parse_mode='HTML')
        else:
            bot.send_message(message.chat.id, "أتمت جميع الطالبات القراءة في هذه القائمة! 🌸")
    else:
        bot.send_message(message.chat.id, "لا توجد قارئات في قائمة الانتظار حالياً 🌸")

# 4. أمر closing لإغلاق ومسح القائمة
@bot.message_handler(commands=['closing', 'إغلاق', 'مسح', 'reset'])
def reset_list(message):
    readers_list.clear()
    listeners_list.clear()
    apologized_list.clear()
    bot.send_message(message.chat.id, "🧹 <b>تم إغلاق ومسح جميع القوائم وبدء حلقة جديدة بنجاح!</b>\n\nأرسل /start لعرض القائمة الجديدة.", parse_mode='HTML')

print("البوت يعمل الآن بالتنسيق المعدل...")
bot.infinity_polling()

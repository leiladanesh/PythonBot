from os import register_at_fork
import random
from gtts import gTTS
import telebot
from khayyam import JalaliDatetime
import qrcode
import pysynth_b
mybot = telebot.TeleBot("2034224355:AAE0g6qFdorFUFgyG6NZZInETwDBT5YfIQo")

@mybot.message_handler(commands=['start'])
def send_welcom(message):
    mybot.send_message (message.chat.id,' سلام خوش آمدی '+ (message.chat.first_name) + ' عزیز 💖')

@mybot.message_handler(commands=['age']) 
def age_func(message):  
    msg = mybot.send_message (message.chat.id,'  . لطفا تاریخ تولد خود را وارد کنید\nمانند    ۱۳۹۰/۱۲/۱۴' )
    mybot.register_next_step_handler(msg,age1)
def age1(message):

    birthday =message.text.split('/')
    if len(birthday )==3:
        diffrence = JalaliDatetime.now() - JalaliDatetime(birthday[0],birthday[1],birthday[2])
        mybot.send_message(message.chat.id,'سن شما '+ str(diffrence.days//365))
    else:
        mybot.reply_to(message,'لطقا تاریخ را درست وارد کنید')       

@mybot.message_handler(commands=['voice'])
def voice_func(message):
    msg = mybot.send_message(message.chat.id,'⌨️ لطفا متن خود را وارد کنید')
    mybot.register_next_step_handler(msg,sound)

def sound (message):
    try:
        message_text = message.text
        language = 'en'
        message_voice = gTTS(text=message_text, lang=language, slow=False)
        message_voice.save('your_voice.ogg')
        voice = open('your_voice.ogg', 'rb')
        mybot.send_voice(message.chat.id, voice)
    except:
        mybot.send_message(message.chat.id, ' دوباره سعی کنید')


@mybot.message_handler(commands=['qrcode'])
def qrcode_func(message):
    msg = mybot.send_message(message.chat.id, 'لطفا متن یا آدرس اینترنتی را وارد کنید ...')
    mybot.register_next_step_handler(msg, qrcode1)
    
def qrcode1(message):
    try:
        message_text = message.text
        qrcode_image = qrcode.make(message_text)
        qrcode_image.save('your_qrcode.png')
        qrCode = open('your_qrcode.png', 'rb')
        mybot.send_photo(message.chat.id, qrCode)
    except:
        mybot.send_message(message.chat.id, 'دوباره تلاش کنید ') 


@mybot.message_handler(commands=['max'])
def max_func(message):
    msg = mybot.send_message(message.chat.id, 'لیستی از اعداد را وارد کنید ','\n اعداد را با(,)از هم جدا کنید')
    mybot.register_next_step_handler(msg, max1)

def max1(message):
    try:
        numbers_text = message.text
        numbers_list = numbers_text.split(',')
        numbers_list = list(map(int, numbers_list))
        answer = str(max(numbers_list))
        mybot.send_message(message.chat.id, f'بزرگترین عدد در لیست {answer}')
    except:
        mybot.send_message(message.chat.id, "نکته:\nعداد را با (,) از هم جدا کنید ")

@mybot.message_handler(commands=['argmax', 'Argmax'])
def argmax(message):
    msg = mybot.send_message(message.chat.id, 'لیستی از اعداد را وارد کنید ','\n اعداد را با(,)از هم جدا کنید')
    mybot.register_next_step_handler(msg, argm)

def argm(message):
    try:
        numbers_text = message.text
        numbers_list = numbers_text.split(',')
        numbers_list = list(map(int, numbers_list))
        answer_1 = str(max(numbers_list))
        answer_2 = str(numbers_list.index(max(numbers_list)))
        mybot.send_message(message.chat.id, f'بزرگترین شما: {answer_1}\nدر خانه: {answer_2}  آرایه است')
    except:
        mybot.send_message(message.chat.id, 'لیستی از اعداد را وارد کنید ','\n اعداد را با(,)از هم جدا کنید')

@mybot.message_handler(commands=['Music'])
def product_music(message):
    msg = mybot.send_message(message.chat.id, "نت موسیقی مورد علاقه ی خود را بفرست تا آهنگ آن را پخش کنم\nExample: ('c', 4), ('e', 4), ('g', 4), ('c5', -2), ('e6', 8), ('d#6', 2)")
    mybot.register_next_step_handler(msg, music)
    
def music(message):
    try:
        test=eval(message.text)
        pysynth_b.make_wav(test, fn = "test.wav")
        song = open('test.wav','rb')
        mybot.send_audio(message.chat.id,song)
    except:
        mybot.send_message(message.chat.id,'متاسفم ُدوباره تلاش کن')            


@mybot.message_handler(commands=['help'])
def help(message):
    Description = '1️⃣ /start : welcom 🥰 \n2️⃣ /help : commands list📜\n3️⃣ /age: calculator your age ⏳ \n4️⃣ /voice : text to voice 🎙\n5️⃣ /max : maximum in list ⚖️ \n6️⃣ /argmax : highest number argument in list\n7️⃣ /qrcode : product QR code 🀡\n8️⃣ /Music : product music 🎼 \n'
    mybot.send_message(message.chat.id, Description)       
   


mybot.polling()
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import json
from json import JSONEncoder
import numpy as np
import face_recognition
from telegram import InputMediaPhoto
TOKEN = ""
ADMIN_ID = 00000



def start_command(update, context):
    # update.message.reply_text(
    #     text=f"Astrum talabalari haqida ma'lumot beruvchi botga xush kelibsiz!{update.message.from_user.first_name} Iltimos ma'lumoti kerak bo'lgan talabaning rasmini tashlang")
    context.bot.send_message(chat_id=ADMIN_ID, text=f"Sizga {update.message.from_user.first_name}dan xabar bor")
    update.message.reply_photo(photo =open("photos/Astrum.jpg", "rb"), caption=f"Astrum talabalari haqida ma'lumot beruvchi botga xush kelibsiz!{update.message.from_user.first_name} Iltimos ma'lumoti kerak bo'lgan talabaning rasmini tashlang")


def message_handler(update, context):
    message = update.message.text
    if message:
        update.message.reply_text(
            text=f"{update.message.from_user.first_name} dastur faqat rasm orqali talabalarning ma'lumotini chiqarib "
                 f"bera oladi!Iltimos rasm jo'nating.")
        context.bot.send_message(chat_id=ADMIN_ID,
                                 text=f"Sizga {update.message.from_user.first_name}dan xabar bor.Xabar:{message}")


def photo_handler(update, context):
    file = update.message.photo[-1].file_id
    obj = context.bot.get_file(file)
    obj.download("photos/Talabalar.jpg")

    with open("../sample.json") as sample_json:
        data = json.load(sample_json)

    known_encode = [np.asarray(i["encode"]) for i in data]
    known_name = [f"{i['dir']} -> {i['name']}" for i in data]

    unkown_picture = face_recognition.load_image_file('photos/Talabalar.jpg')
    unkown_encode = face_recognition.face_encodings(unkown_picture)[0]


    TAL = face_recognition.api.compare_faces(known_encode, unkown_encode, tolerance=0.5)
    if True not in TAL:
        update.message.reply_text(f"Bu o'quvchi bizda yo'q")
    for aa, i in enumerate(TAL):
        if i:
            update.message.reply_text(f"{known_name[aa]}")


def main():
    updater = Updater(token=TOKEN)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start_command))
    dispatcher.add_handler(MessageHandler(Filters.text, message_handler))
    dispatcher.add_handler(MessageHandler(Filters.photo, photo_handler))

    updater.start_polling()
    updater.idle()


main()

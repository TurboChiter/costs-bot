# -*- coding: utf-8 -*-

import time
import database as db
import os
from aiogram import Bot
from aiogram import types
from aiogram import Dispatcher
from aiogram import executor
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

#FSM - машина состояний
class Form(StatesGroup):
    name = State()
    age = State()
    gender = State()
    photo = State()
    find = State()
    like = State()
    #interest = State()

#Основные переменные
TOKEN = "5017005570:AAHDwQN7cBhOsDUE5lsE6TQWmkBzyIH7icc"
bot = Bot(token=TOKEN)

dp = Dispatcher(bot, storage=MemoryStorage())

#Кнопки
gendermarkup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
gendermarkup.add("Парней", "Девушек")
gendermarkup.add("Всё равно")
menu = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
menu.add("Моя Анкета📝", "Смотреть Анкеты📝")
menu.add("Удалить анкету❌")
findanket = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
findanket.add("❤️", "Следующая Анкета📝")
findanket.add("Назад в меню◀️")
startmarkup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
startmarkup.add("Старт")
#menu.add("")
#interestmarkup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
#interestmarkup.add("Парней", "Девушек")
#interestmarkup.add("Мне всё равно")

#Функции бота
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    userid = message.from_user.id
    if not db.check(userid):
        await bot.send_message(message.chat.id, "Привет, для того что бы начать пользоваться ботом нужно пройти регистрацию, напишите /register")
    else:
        await bot.send_message(message.chat.id, "Вы уже зарегестрированы!", reply_markup=menu)

"""@dp.message_handler(commands=['delete'])
async def start(message: types.Message):
    userid = message.from_user.id
    db.delete(userid)
    await bot.send_message(message.chat.id, "Ваша анкета удалена!", reply_markup=types.ReplyKeyboardRemove())"""

#---------------------------------------------------------------------------------------------------------------------------------------
#Команда для регистрации
@dp.message_handler(commands=['register'], state=None)
async def register(message: types.Message):
    userid = message.from_user.id
    isregistered = db.check(userid)
    if not isregistered:
        await message.answer("Вы начали регистрацию.\nВведите ваше имя:", reply_markup=types.ReplyKeyboardRemove())
        await Form.name.set()
    elif isregistered:
        await bot.send_message(message.chat.id, "Вы уже зарегестрированы!", reply_markup=menu)


@dp.message_handler(state=Form.name)
async def username(message: types.Message, state: FSMContext):
    userid = message.from_user.id
    time.sleep(1)
    if len(message.text) <= 20:
        db.newuser(userid)
        db.setname(userid, message.text)
        await bot.send_message(message.chat.id, "Теперь укажите возраст: ")
        await Form.next()
    else:
        await bot.send_message(message.chat.id, "Слишком длинное имя! Попробуйте ещё раз.")
        return


@dp.message_handler(state=Form.age)
async def age(message: types.Message, state: FSMContext):
    userid = message.from_user.id
    print(type(message.text))
    if len(message.text) <= 3:
        try:
            int(message.text)
            db.setage(userid, int(message.text))
            await bot.send_message(message.chat.id, "Кого ты ищешь?", reply_markup=gendermarkup)
            await Form.next()
        except Exception:
            await bot.send_message(message.chat.id, "Используйте только цифры!")
            return
    else:
        await bot.send_message(message.chat.id, "Укажите настоящий возраст! Попробуйте ещё раз.")
        return


@dp.message_handler(state=Form.gender)
async def gender(message: types.Message, state: FSMContext):
    userid = message.from_user.id
    if message.text == "Парней":
        db.setgender(userid, message.text)
        await Form.next()
        await bot.send_message(message.chat.id, "Теперь пришли фотографию...", reply_markup=types.ReplyKeyboardRemove())
    elif message.text == "Девушек":
        db.setgender(userid, message.text)
        await Form.next()
        await bot.send_message(message.chat.id, "Теперь пришли фотографию...", reply_markup=types.ReplyKeyboardRemove())
    elif message.text == "Всё равно":
        db.setgender(userid, "Всё равно")
        await Form.next()
        await bot.send_message(message.chat.id, "Теперь пришли фотографию...", reply_markup=types.ReplyKeyboardRemove())
    else:
        await bot.send_message(message.chat.id, "Нет такого варианта ответа.")
        return

@dp.message_handler(content_types=['document', 'photo'], state=Form.photo)
async def getphoto(message: types.Message, state=FSMContext):
    userid = message.from_user.id
    if message.document:
        userfile = await bot.get_file(message.document.file_id)
        userfile = userfile.file_path
        await bot.download_file(userfile, str(userid) + ".png")
        await state.finish()
        await bot.send_message(message.chat.id, "Регистрация прошла успешно!", reply_markup=types.ReplyKeyboardRemove())
        await bot.send_message(message.chat.id, "Приятного пользования! :)", reply_markup=menu)
        #await bot.send_message(message.chat.id, "Кого ты ищешь?", reply_markup=interestmarkup)
    elif message.photo.pop:
        userfile2 = await message.photo.pop().download('F:/Бот/' + str(userid) + ".png")
        await state.finish()
        await bot.send_message(message.chat.id, "Регистрация прошла успешно!", reply_markup=types.ReplyKeyboardRemove())
        await bot.send_message(message.chat.id, "Приятного пользования! :)", reply_markup=menu)

"""@dp.message_handler(content_types=['text'], state=Form.interest)
async def interestuser(message: types.Message, state=FSMContext):
    userid = message.from_user.id
    if message.text == "Парней":
        db.setinterest(userid, "Парень")
        await state.finish()
        await bot.send_message(message.chat.id, "Регистрация прошла успешно!", reply_markup=types.ReplyKeyboardRemove())
        await bot.send_message(message.chat.id, "Приятного пользования! :)", reply_markup=menu)
    elif message.text == "Девушек":
        db.setinterest(userid, "Девушка")
        await state.finish()
        await bot.send_message(message.chat.id, "Регистрация прошла успешно!", reply_markup=types.ReplyKeyboardRemove())
        await bot.send_message(message.chat.id, "Приятного пользования! :)", reply_markup=menu)
    elif message.text == "Мне всё равно":
        db.setinterest(userid, "Другое")
        await state.finish()
        await bot.send_message(message.chat.id, "Регистрация прошла успешно!", reply_markup=types.ReplyKeyboardRemove())
        await bot.send_message(message.chat.id, "Приятного пользования! :)", reply_markup=menu)
    else:
        await bot.send_message(message.chat.id, "Нет такого варианта ответа.")
        return"""

@dp.message_handler(state=Form.find)
async def next(message: types.Message, state=FSMContext):
    #global userid1
    userid = message.from_user.id
    name, age, gender = db.getfullinfo(userid)
    if message.text == "Следующая Анкета📝":
        userid1 = db.randomuser(userid, gender[0], age[0])
        name, age, gender = db.getfullinfo(userid1)
        db.setuserid1(userid1, userid)
        await bot.send_photo(message.chat.id, open(str(userid1) + ".png", 'rb'), "Имя: " + str(name[0]) + ", Возраст: " + str(age[0]) + ".", reply_markup=findanket) # + ", Пол: " + str(gender[0])
        return
    elif message.text == "❤️":
        userid1 = db.checkuserid1(userid)
        db.like(userid1, userid)
        userid1 = db.randomuser(userid, gender[0], age[0])
        name, age, gender = db.getfullinfo(userid1)
        db.setuserid1(userid1, userid)
        await bot.send_photo(message.chat.id, open(str(userid1) + ".png", 'rb'), "Имя: " + str(name[0]) + ", Возраст: " + str(age[0]) + ".", reply_markup=findanket) # + ", Пол: " + str(gender[0])
        return
    elif message.text == "Старт":
        #await bot.send_message(message.chat.id, "Вы начали просмотр анкет:", reply_markup=findanket)
        #time.sleep(1)
        return
    if message.text == "Назад в меню◀️":
        await bot.send_message(message.chat.id, "Ждём пока кто то увидит вашу анкету...", reply_markup=menu)
        await state.finish()

#---------------------------------------------------------------------------------------------------------------------------------------
#Просмотр своей анкеты
@dp.message_handler()
async def myanket(message: types.Message):
    userid = message.from_user.id
    name, age, gender = db.getfullinfo(userid)
    if db.check(userid):
        #interest = db.getinterest(userid)
        if message.text == "Моя Анкета📝":
            await bot.send_photo(message.chat.id, open(str(userid) + ".png", 'rb'), caption="Имя: " + str(name[0]) + ", Возраст: " + str(age[0]) + ", Пол: " + str(gender[0]) + ".", reply_markup=menu)
            #await bot.send_message(message.chat.id, "Имя: " + str(name[0]) + ", Возраст: " + str(age[0]) + ", Пол: " + str(gender[0]) + ".")
        elif message.text == "Смотреть Анкеты📝":
            #await bot.send_message(message.chat.id, "Что бы начать нажмите кнопку Старт.", reply_markup=startmarkup)
            userid1 = db.randomuser(userid, gender[0], age[0])
            if userid1 != None:
                name, age, gender = db.getfullinfo(userid1)
                db.setuserid1(userid1, userid)
                await bot.send_photo(message.chat.id, open(str(userid1) + ".png", 'rb'), "Имя: " + str(name[0]) + ", Возраст: " + str(age[0]) + ".", reply_markup=findanket) # + ", Пол: " + str(gender[0])
                await Form.find.set()
            else:
                await bot.send_message(message.chat.id, "Не удалось никого найти по твоим интересам :(")
        elif message.text == "Удалить анкету❌":
            userid = message.from_user.id
            os.remove("F:/Бот/" + str(userid) + ".png")
            db.delete(userid)
            await bot.send_message(message.chat.id, "Ваша анкета удалена!", reply_markup=types.ReplyKeyboardRemove())
        else:
            await bot.send_message(message.chat.id, "Я тебя не понимаю :(", reply_markup=menu)
    else:
        await bot.send_message(message.chat.id, "Привет, для того что бы начать пользоваться ботом нужно пройти регистрацию, напишите /register")

#Бесконечный цикл, (Работа бота)
if __name__ == '__main__':
    executor.start_polling(dp)
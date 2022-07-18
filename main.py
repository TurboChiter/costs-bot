# -*- coding: utf-8 -*-

import time
import datetime
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
    add = State()
    rem = State()
    limit = State()

#Основные переменные
TOKEN = "5596490225:AAEKneSiqKW6JOXH4j12zfiZh6maT2GhEaI"
bot = Bot(token=TOKEN)

dp = Dispatcher(bot, storage=MemoryStorage())

#Кнопки
menu = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
menu.add("Общие рассходы📝", "Потрачено сегодня📝")
menu.add("Отнять сумму➖", "Добавить сумму➕")
menu.add("Установить лимит")

menu2 = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
menu2.add("Назад")

#Функции бота
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    userid = message.from_user.id
    if not db.check(userid):
        await bot.send_message(message.chat.id, "Привет, для того что бы начать пользоваться ботом нужно пройти регистрацию, напишите /register")
    else:
        await bot.send_message(message.chat.id, "Вы уже зарегестрированы!", reply_markup=menu)


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
        await state.finish()
        await bot.send_message(message.chat.id, "Регистрация прошла успешно!", reply_markup=types.ReplyKeyboardRemove())
        await bot.send_message(message.chat.id, "Приятного пользования, " + message.text + "! :)", reply_markup=menu)
    else:
        await bot.send_message(message.chat.id, "Слишком длинное имя! Попробуйте ещё раз.")
        return

@dp.message_handler(state=Form.add)
async def username(message: types.Message, state: FSMContext):
    userid = message.from_user.id
    if message.text == "Назад":
        await bot.send_message(message.chat.id, "Меню:", reply_markup=menu)
        await state.finish()
    else:
        try:
            int(message.text)
            name, costs, ta, datereg, limit, lastuse = db.getfullinfo(userid)
            db.setcosts(userid, costs + int(message.text))
            db.setta(userid, ta + int(message.text))
            name, costs, ta, datereg, limit, lastuse = db.getfullinfo(userid)
            if costs == limit:
                await bot.send_message(message.chat.id, "❗️ Внимание! Вы достигли лимита на день. ❗️", reply_markup=menu)
                await bot.send_message(message.chat.id, "Успешно добавлено✅", reply_markup=menu)
                await state.finish()
            elif costs > limit:
                await bot.send_message(message.chat.id, "❗️ Внимание! Вы привысили лимит на день. ❗️", reply_markup=menu)
                await bot.send_message(message.chat.id, "Успешно добавлено✅", reply_markup=menu)
                await state.finish()
            else:
                await bot.send_message(message.chat.id, "Успешно добавлено✅", reply_markup=menu)
                await state.finish()
        except Exception:
            await bot.send_message(message.chat.id, "Используйте только цифры!")
            return

@dp.message_handler(state=Form.rem)
async def username(message: types.Message, state: FSMContext):
    userid = message.from_user.id
    if message.text == "Назад":
        await bot.send_message(message.chat.id, "Меню:", reply_markup=menu)
        await state.finish()
    else:
        try:
            int(message.text)
            name, costs, ta, datereg, limit, lastuse = db.getfullinfo(userid)
            if costs - int(message.text) >= 0:
                db.setcosts(userid, costs - int(message.text))
                db.setta(userid, ta - int(message.text))
                await bot.send_message(message.chat.id, "Успешно убавлено✅", reply_markup=menu)
                await state.finish()
            else:
                await bot.send_message(message.chat.id, "Вы ввели не правильную сумму!")
                return
        except Exception:
            await bot.send_message(message.chat.id, "Используйте только цифры!")
            return

@dp.message_handler(state=Form.limit)
async def username(message: types.Message, state: FSMContext):
    userid = message.from_user.id
    if message.text == "Назад":
        await bot.send_message(message.chat.id, "Меню:", reply_markup=menu)
        await state.finish()
    else:
        try:
            int(message.text)
            db.setlimit(userid, int(message.text))
            await bot.send_message(message.chat.id, "Лимит установлен✅", reply_markup=menu)
            await state.finish()
        except Exception:
            await bot.send_message(message.chat.id, "Используйте только цифры!")
            return

#Реакции на кнопки
@dp.message_handler()
async def buttons(message: types.Message):
    userid = message.from_user.id
    name, costs, ta, datereg, limit, lastuse = db.getfullinfo(userid)
    if int(lastuse.split(" ")[0].replace("-", "")) < int(str(datetime.datetime.today()).split(" ")[0].replace("-", "")):
        db.setcosts(userid, 0)
        db.setlastuse(userid, str(datetime.datetime.today()).split(" ")[0].replace("-", ""))
        name, costs, ta, datereg, limit, lastuse = db.getfullinfo(userid)
        if message.text == "Общие рассходы📝":
            await bot.send_message(message.chat.id, name + ", начиная с " + str(datereg) + " вы потратили " + str(ta) + " грн.", reply_markup=menu)
        elif message.text == "Отнять сумму➖":
            await bot.send_message(message.chat.id, "Укажите сумму (грн):", reply_markup=menu2)
            await Form.rem.set()
        elif message.text == "Добавить сумму➕":
            await bot.send_message(message.chat.id, "Укажите сумму (грн):", reply_markup=menu2)
            await Form.add.set()
        elif message.text == "Потрачено сегодня📝":
            if costs == limit:
                await bot.send_message(message.chat.id, "❗️ Внимание! Вы достигли лимита на день. ❗️", reply_markup=menu)
                await bot.send_message(message.chat.id, name + ", сегодня вы потратили " + str(costs) + "/" + str(limit) + " грн.", reply_markup=menu)
            elif costs > limit:
                await bot.send_message(message.chat.id, "❗️ Внимание! Вы привысили лимит на день. ❗️", reply_markup=menu)
                await bot.send_message(message.chat.id, name + ", сегодня вы потратили " + str(costs) + "/" + str(limit) + " грн.", reply_markup=menu)
            else:
                await bot.send_message(message.chat.id, name + ", сегодня вы потратили " + str(costs) + "/" + str(limit) + " грн.", reply_markup=menu)
        elif message.text == "Установить лимит":
            await bot.send_message(message.chat.id, "Лимит рассходов: " + str(limit) + " грн.")
            await bot.send_message(message.chat.id, "Укажите сумму (грн):", reply_markup=menu2)
            await Form.limit.set()
    else:
        name, costs, ta, datereg, limit, lastuse = db.getfullinfo(userid)
        if message.text == "Общие рассходы📝":
            await bot.send_message(message.chat.id, name + ", начиная с " + str(datereg) + " вы потратили " + str(ta) + " грн.", reply_markup=menu)
        elif message.text == "Отнять сумму➖":
            await bot.send_message(message.chat.id, "Укажите сумму (грн):", reply_markup=menu2)
            await Form.rem.set()
        elif message.text == "Добавить сумму➕":
            await bot.send_message(message.chat.id, "Укажите сумму (грн):", reply_markup=menu2)
            await Form.add.set()
        elif message.text == "Потрачено сегодня📝":
            if costs == limit:
                await bot.send_message(message.chat.id, "❗️ Внимание! Вы достигли лимита на день. ❗️", reply_markup=menu)
                await bot.send_message(message.chat.id, name + ", сегодня вы потратили " + str(costs) + "/" + str(limit) + " грн.", reply_markup=menu)
            elif costs > limit:
                await bot.send_message(message.chat.id, "❗️ Внимание! Вы привысили лимит на день. ❗️", reply_markup=menu)
                await bot.send_message(message.chat.id, name + ", сегодня вы потратили " + str(costs) + "/" + str(limit) + " грн.", reply_markup=menu)
            else:
                await bot.send_message(message.chat.id, name + ", сегодня вы потратили " + str(costs) + "/" + str(limit) + " грн.", reply_markup=menu)
        elif message.text == "Установить лимит":
            await bot.send_message(message.chat.id, "Лимит рассходов: " + str(limit) + " грн.")
            await bot.send_message(message.chat.id, "Укажите сумму (грн):", reply_markup=menu2)
            await Form.limit.set()

#Бесконечный цикл, (Работа бота)
if __name__ == '__main__':
    executor.start_polling(dp)
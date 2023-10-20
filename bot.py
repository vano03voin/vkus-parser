from os import getenv
from async_main import collect_data
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiofiles import os
import requests
import time
import asyncio
from datetime import datetime
bot = Bot(token='UR TOCKEN HERE')
dp = Dispatcher(bot)
import random


async def send_data( chat_id=''):
    global items
    global iswork
    global banlist
    global mid
    names = await collect_data()
    for i in range(len(names)):
        if i%2 == 0 and names[i] not in items and names[i] not in banlist:
            items.append(names[i])
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(types.InlineKeyboardButton(text="бан", callback_data="ban"))
            mid.append((await bot.send_photo(chat_id=chat_id, photo=requests.get(names[i+1]).content, caption=names[i],reply_markup=keyboard)))
            print(str(names[i][:10])+' added')
        else:
            if i%2 == 0:
                print(str(names[i][:10])+' exist')
    for i in items:
        if i not in names:
            items.remove(i)
            for g in mid:
                if g.caption==i:
                    print(str(g.caption[:10])+' delet')
                    await bot.delete_message(g.chat.id,g.message_id)
                    await asyncio.sleep(1)
                    mid.remove(g)
    time=datetime.now()
    print(str('items: ')+str(len(items)))
    if len(items) != len(mid):
        print(str('links: ')+str(len(mid)))
        mlinks='items '
        for i in items:
            if i%2==0:
                mlinks+=','+str(i.caption[:10])
        print(mlinks)
        mlinks='links '
        for i in mid:
            mlinks+=','+str(i.caption[:10])
        print(mlinks)
    print(str(time.strftime("%H:%M")))
    iswork=False

@dp.callback_query_handler(text="ban")
async def adInBan(call: types.CallbackQuery):
    global banlist
    global mid
    global items
    banlist.append(call.message.caption)
    for g in mid:
        if g.caption==call.message.caption:
            items.remove(call.message.caption)
            print(str(g.caption[:10])+' delet')
            mid.remove(g)
            break
    await bot.delete_message(call.message.chat.id , call.message.message_id)

@dp.message_handler(Text(equals='Dump'))
async def Dump(message: types.Message):
    global items
    global banlist
    with open(f'ban.txt','w', encoding = 'utf-8') as file:
        for i in banlist:
            file.write(str(i)+',')
    await message.answer('ok')

@dp.message_handler(Text(equals='Update'))
async def Update(message: types.Message):
    global iswork
    if iswork == False:
        iswork = True
        chat_id = message.chat.id
        await send_data( chat_id=chat_id)

@dp.message_handler(commands='start')
async def start(message: types.Message):
    global iswork
    start_buttons = ['Update', 'Dump']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    await message.answer('started', reply_markup=keyboard)
    while True:
        iswork = True
        chat_id = message.chat.id
        await send_data( chat_id=chat_id)
        await asyncio.sleep(random.randint(400, 500))


mid=[]#ссылки на текущие смс
items=[]#четные названия, не чет - ссылки
iswork=False
with open(f'ban.txt','r', encoding = 'utf-8') as file:
    banlist=list(file.read()[:-1].split(','))
cookies={'Your cocies': 'here'}
executor.start_polling(dp)

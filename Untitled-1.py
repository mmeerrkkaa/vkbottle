import logging
import os
import random
from typing import Optional
from vkbottle import *
from vkbottle.bot import Bot, Message
from vk_api import VkApi
import sqlite3
from command import profile
from itemsFolder import items, item
import json

bot = Bot("070cfc361b1836495112be381de766e54cfe0361cba2812d69895811e0834e87e52a1a6ca6ff69cb02426")
# https://vk.com/club200829250



logging.basicConfig(level=logging.INFO)
KEYBOARD = Keyboard(one_time=True).add(Text("123", {"cmd": "reg"})).get_json()
menu = keyboard=(
        Keyboard(one_time=True, inline=False)
        .add(Text("📒 Профиль", {"cmd": "profile"}))
        .add(Text("📦 Инвентарь", {"cmd": "invent"}))
        ).get_json()




@bot.on.message(text=["начать", "меню"])
@bot.on.message(payload={"cmd": "menu"})
async def start(message: Message):
    cursor.execute(f"SELECT id_member FROM users where id_member={int(message.peer_id)}")#все также, существует ли участник в БД
    if cursor.fetchone()==None:#Если не существует
        await message.answer(
    message="Ваш профиль не зарегестрирован",
    keyboard=(
        Keyboard(one_time=True, inline=False)
        .add(Text("Зарегестрироваться", payload={"cmd": "reg"}))
    ).get_json()
)
    else:
        await message.answer(f"Привет, {profile.GetProfile(message)[1]}!",keyboard=menu)

@bot.on.message(payload={"cmd": "reg"})
async def regs(message: Message):
    nick = await bot.api.users.get(user_ids=message.from_id)
    await message.answer(profile.registration(message, f"{nick[0].last_name}_{nick[0].first_name}"))

    await start(message)

@bot.on.message(payload={"cmd": "profile"})
async def profiles(message: Message):
    await message.answer(profile.info(message))
    await message.answer(
    message="Вы в <<Профиль>>",
    keyboard=(
        Keyboard(one_time=True, inline=False)
        .add(Text("Подробнее", payload={"cmd": "GetProfile"}))
        .add(Text("На главную", payload={"cmd": "menu"}))
    ).get_json()
)
    
@bot.on.message(payload={"cmd": "GetProfile"})
async def GetProfiles(message: Message):
    profiles = profile.GetProfile(message)
    wars = json.loads(profiles[6])
    await message.answer(f"""Урон: {wars[1]}
    Броня: {wars[2]}
    Шанс уклонения: {wars[3]} %
    Шанс крит удара: {wars[4]} %""")
    await start(message)




@bot.on.message(payload={"cmd": "invent"})
async def inventary(message: Message):
    keyinv = Keyboard(one_time=True, inline=False)

    invet = profile.GetInv(message)

 #   await message.answer(profile.sendInv(message))
    if len(invet) == 0:
        await message.answer("Инвентарь пуст")
        await start(message)
        return 0

    countKey = 0
    for i in invet:
        if countKey < 9:
            keyinv.add(Text(i['name'],payload={"cmd": "item", "item": i["name"]}))
            keyinv.row()
            countKey += 1
        else:
            break
    keyinv.add(Text(f"В меню", payload={"cmd": "menu"}))
    await message.answer(message=profile.sendInv(message),keyboard=keyinv.get_json())
    



#@bot.on.message(text=["Распаковать <item>"])
@bot.on.message(payload_map={"cmd": "unpack", "item": str, "count": int})
async def unpacks(message: Message):
    item = message.get_payload_json()["item"]
    count = message.get_payload_json()["count"]
    await message.answer(items.itemUnPack(message, item, count))
    await message.answer(items.removeItem(message, item, count))
    await start(message)

@bot.on.message(payload_map={"cmd": "DropItem", "item": str, "count": int})
async def DropItems(message: Message):
    item = message.get_payload_json()["item"]
    count = message.get_payload_json()["count"]
    await message.answer(items.removeItem(message, item, count))
    await inventary(message)



@bot.on.message(text=["item <item>"])
@bot.on.message(payload_map={"cmd": "item", "item": str})
async def finditem(message: Message, item: Optional[str] = None):
    item = message.get_payload_json()["item"]

    if item is None:
        print(1)
        return 0
    
    fin = items.findItem(message, item)
    
    if fin[1]["type"] == "коробка":

        keyinv = Keyboard(one_time=True, inline=False)
        keyinv.add(Text(f"Распаковать", payload={"cmd": "unpack", "item": item, "count": 1}))
        if fin[1]["count"] > 1:
            keyinv.add(Text(f"Распаковать Все {fin[1]['count']}", payload={"cmd": "unpack", "item": item, "count": int(fin[1]["count"])}))
        keyinv.row()
        keyinv.add(Text("Назад", payload={"cmd": "invent"}))
        await message.answer(fin[0], keyboard = keyinv)

    elif fin[1]["type"] == "броня":
        await message.answer("кнопок надеть пока нету. Те введут в меню")
        await message.answer(
        message=fin[0],
        keyboard=(
            Keyboard(one_time=True, inline=False)
            .add(Text(f"Надеть {item}", payload={"cmd": f"menu"}))
            .add(Text(f"Выкинуть", payload={"cmd": "DropItem", "item": item, "count": int(fin[1]["count"])+1}))
            .row()
            .add(Text("Назад", payload={"cmd": "invent"}))
    ).get_json()
    )

    elif fin[1]["type"] == "оружие":
        await message.answer("кнопок надеть пока нету. Те кнопки введут в меню")
        await message.answer(
        message=fin[0],
        keyboard=(
            Keyboard(one_time=True, inline=False)
            .add(Text(f"Надеть {item}", payload={"cmd": f"menu"}))
            .add(Text(f"Выкинуть", payload={"cmd": "DropItem", "item": item, "count": int(fin[1]["count"])+1}))
            .row()
            .add(Text("Назад", payload={"cmd": "invent"}))
    ).get_json()
    )

    else:         
        await message.answer(fin[0])
    

@bot.on.message(payload_map={"cmd": "tests", "item": str})
async def testbut(message: Message):
    await message.answer(message.get_payload_json()["item"])

@bot.on.message(text=["test"])
async def test(message: Message):
    itemd = item.data["Подарок новичка"]
    print(items.addItem(message, itemd, 5))
    await start(message)

conn = sqlite3.connect("Vk.db") # или :memory:
cursor = conn.cursor()


cursor.execute(f"DROP TABLE IF EXISTS users;")
cursor.execute(f"CREATE TABLE users(ids INTEGER PRIMARY KEY NOT NULL,nick TEXT, id_member INTEGER, lvl INTEGER, xp INTEGER, hp INTEGER, war TEXT, countItem INTEGER, inv TEXT, money INTEGER);")
conn.commit()

#cursor.execute(f"CREATE TABLE будущий аукцион();")


bot.run_forever()
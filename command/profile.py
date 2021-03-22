import sqlite3
import json

import sys
# '/path/to/application/app/items'
sys.path.insert(0, './itemsFolder')
import item

#sqliteAdd = json.dumps(membId)

def info(message):
    cursor.execute(f"SELECT * FROM users where id_member={message.peer_id}")
    info = cursor.fetchone()
    num = info[9]
    gold = num // 1000
    ag = (num % 1000) // 100
    med = num % 100
    wars = json.loads(info[6])
    return f"""Ник: {info[1]}
    Уровень: {info[3]}
    Хп: {wars[0]}
    Денег: Золотых монет: {gold}, Серебрянных монет: {ag}, Медных монет: {med}"""


def registration(message, nick):
    war = [10 ,1 ,0, 0, 0] # хп, дамаг, броня, шанс уворота, шанс крит демеджа
    sqliteAdd = json.dumps(war)

    gift = ["Коробка со слабой рапирой жизни"]
    inv = []
    gifts = ""
    for i in gift:
        inv.append(item.data[i])
        gifts += f"<<{i}>> x1\n"
    inv = json.dumps(inv)

    cursor.execute(f"INSERT INTO users VALUES (NULL,'{nick}',{int(message.peer_id)}, '1', '0', '0', '{sqliteAdd}', '10', '{inv}', '0')")
    conn.commit()


    return f"ваш профиль успешно зарегестрирован!\nПолучены предметы:\n{gifts}"

def GetProfile(message):
    cursor.execute(f"SELECT * FROM users where id_member={message.from_id}")
    info = cursor.fetchone()
    return info


def sendInv(message):
    profiles = GetProfile(message)
    inv = json.loads(profiles[8])
    text = f"{len(inv)}/{profiles[7]}:\n"
    for i in inv:
        if i["quality"] != "коробка":
            text += f"[{i['quality']}] {i['name']}"
        else:
            text += f"{i['name']}"
        if i["count"] != 0:
            text += f" x{i['count']}"
        text += "\n"
    return text

def GetInv(message):
    profiles = GetProfile(message)
    inv = json.loads(profiles[8])
    return inv

conn = sqlite3.connect("Vk.db") # или :memory:
cursor = conn.cursor()

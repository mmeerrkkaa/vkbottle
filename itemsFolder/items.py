import sys
import item
import json
import sqlite3
# '/path/to/application/app/items'
sys.path.insert(0, './command')
import profile
import ast

data = item.data


def findItem(message, item):
    invet = profile.GetInv(message)
    for i in invet:
        if i["name"] == item:
            if i["type"] == "коробка":
                text = f"""Имя: {i["name"]}
                Тип: {i["type"]}
                Описание: {i["desc"]}"""
                if i["sell"] > 0:
                    num = i["sell"]
                    text += f"\nЦена: Золотых монет: {num // 1000}, Серебрянных монет: {(num % 1000) // 100}, Медных монет: {num % 100}"

            elif i["type"] == "оружие":
                text = f"""Имя: {i["name"]}
                Тип: {i["type"]}
                Качество: {i["quality"]}
                Описание: {i["desc"]}
                Урон: {i["damage"]}"""
                if i["sell"] > 0:
                    num = i["sell"]
                    text += f"\nЦена: Золотых монет: {num // 1000}, Серебрянных монет: {(num % 1000) // 100}, Медных монет: {num % 100}"

            elif i["type"] == "броня":
                text = f"""Имя: {i["name"]}
                Тип: {i["type"]}
                Качество: {i["quality"]}
                Описание: {i["desc"]}
                броня: {i["armor"]}"""
                if i["sell"] > 0:
                    num = i["sell"]
                    text += f"\nЦена: Золотых монет: {num // 1000}, Серебрянных монет: {(num % 1000) // 100}, Медных монет: {num % 100}"

            if len(i["особенности"]) != 0:
                text += f"\nОсобенности:\n"

                for qu in i["особенности"]:
                    text += f"{qu}: {i['особенности'][qu]}\n"
            break
    return text, i

def itemUnPack(message, item):
    invet = profile.GetInv(message)
    

    adds = ""
    for i in invet:
        if i["name"] == str(item):

            for q in i["add"]:
              #  print(item.data[q])
                invet.append(data[q])

                adds += f'{q}\n'

            invet.remove(i)
            break
    
    invAdd = json.dumps(invet)
    cursor.execute('UPDATE users SET inv=(?) where id_member=(?)', (invAdd, message.peer_id))
    conn.commit()
    if len(adds) == 0:
        return "У вас нет этого предмета"
    return f"получено:\n{adds}"


def addItem(message, itemd, count):

    memb = profile.GetProfile(message)
    inv = json.loads(memb[8])
    nex = True
    
        

    if itemd["count"] == 0:
        if len(inv) >= len(memb[7]):
            return "инвентарь полон"

    else:
        for i in inv:
            if i["name"] == itemd["name"]:
                inv[inv.index(i)]["count"] += count
                print("yes")
                nex = False
                break
    if nex == True:
        inv.append(itemd)
            
    
    
    invAdd = json.dumps(inv)
    cursor.execute('UPDATE users SET inv=(?) where id_member=(?)', (invAdd, message.peer_id))
    conn.commit()

    return "1"





conn = sqlite3.connect("Vk.db") # или :memory:
cursor = conn.cursor()
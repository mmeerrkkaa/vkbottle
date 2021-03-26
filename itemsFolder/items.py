import sys
import item
import json
import sqlite3
import random
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

def itemUnPack(message, item, count = 1, cpack = 1):
    invet = profile.GetInv(message)
    print(count, cpack)
    num = 0
    for i in range(cpack):
        adds = ""
        for i in invet:
            if i["name"] == str(item):
              #  invet.remove(i) # не раб
                for q in i["add"]:

                #  print(item.data[q])
                    if type(q) != int and addItem(message, data[q], count):
                        adds += f'{q} x{count}\n'

                    
                    #invet.append(data[q])
                    if type(q) == int:
                        for dsad in range(count):
                        
                            if q < 0:
                                num += random.randint(1, abs(q))
                            else:
                                num += q
    

                
                break
    
    if num != 0:
        cursor.execute(f"SELECT money FROM users where id_member={message.peer_id}")
        moneyuser = cursor.fetchone()
        gold = num // 1000
        ag = (num % 1000) // 100
        med = num % 100
        cursor.execute(f'UPDATE users SET money={moneyuser[0]+num} where id_member={message.peer_id}')
        conn.commit()

                    
        adds += f"Монеты: Золотых: {gold}, Серебрянных: {ag}, Медных: {med}"


    if len(adds) == 0:
        return "У вас нет этого предмета"
    return f"получено:\n{adds}"


def addItem(message, itemd, count):

    count += itemd["count"]
    memb = profile.GetProfile(message)

    inv = json.loads(memb[8])
    nex = True
    
    print(len(inv), memb[7])
    if len(inv) >= memb[7]:
        return "инвентарь полон"

    elif itemd["count"] == 0:
        for _ in range(count):
            inv.append(itemd)
            nex = False

    else:
        for i in inv:
            if i["name"] == itemd["name"]:
                inv[inv.index(i)]["count"] += count
                print("yes")
                nex = False                    
                break
    if nex == True:
        itemd["count"] = count
        inv.append(itemd)
            
    
    
    invAdd = json.dumps(inv)
    cursor.execute('UPDATE users SET inv=(?) where id_member=(?)', (invAdd, message.peer_id))
    conn.commit()

    return "1"


def removeItem(message, itemd, count):
    print(123)
    memb = profile.GetProfile(message)
    inv = json.loads(memb[8])
    for x in inv:
        if x["name"] == itemd:
            itemd = x
            break
    nex = True

    if itemd["count"] == 0 or itemd["count"] == 1:
        for _ in range(count):
            inv.remove(itemd)

    else:
        for i in inv:
            if i["name"] == itemd["name"]:

                if inv[inv.index(i)]["count"]-count > 1: 
                    inv[inv.index(i)]["count"] -= count
                    print("yes")
                    nex = False                    
                    break
                else:
                    inv.remove(itemd)
                    break

            
    
    
    invAdd = json.dumps(inv)
    cursor.execute('UPDATE users SET inv=(?) where id_member=(?)', (invAdd, message.peer_id))
    conn.commit()

    
    return f"Удалено: {itemd['name']} {count} шт"




conn = sqlite3.connect("Vk.db") # или :memory:
cursor = conn.cursor()
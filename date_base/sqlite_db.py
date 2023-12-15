import sqlite3 as sq
import pandas as pd
from create_bot import bot


def sql_start():
    global base, cur, base1, cur1, base2, cur2

    base = sq.connect('patients.db')
    base1 = sq.connect('quality_oms.db')
    base2 = sq.connect('quality_dms.db')
    cur = base.cursor()
    cur1 = base1.cursor()
    cur2 = base2.cursor()

    if base:
        print('База данных подключена')
    base.execute(
        '''CREATE TABLE IF NOT EXISTS patients(id INT PRIMARY KEY, unit TEXT, medical_case INT, referral TEXT, 
        reason TEXT)'''
    )
    base.commit()

    base1.execute(
        '''CREATE TABLE IF NOT EXISTS quality_oms(
        id INT PRIMARY KEY, unit TEXT, conditions INT, diagnostics INT,
        free_medicines INT, information INT, doctor INT, nurse INT, orderly INT,
        placement INT, nutrition INT, treatment INT, general INT
        )'''
    )
    base1.commit()

    base2.execute(
        '''CREATE TABLE IF NOT EXISTS quality_dms(
        id INT PRIMARY KEY, consultation INT, operation INT, anesthesia INT,
        other INT, diagnostics INT, analyzes INT, devices INT, simple_devices INT,
        drugs INT, hygienic INT, ward INT, nothing_choice INT
        )'''
    )
    base2.commit()


async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO patients VALUES (?, ?, ?, ?, ?)', tuple(data.values()))
        base.commit()


async def sql_add_command_quality_oms(state):
    async with state.proxy() as data:
        cur1.execute('INSERT INTO quality_oms VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                    tuple(data.values()))
        base1.commit()


async def sql_add_command_quality_dms(state):
    async with state.proxy() as data:
        cur2.execute('INSERT INTO quality_dms VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                    tuple(data.values()))
        base2.commit()


async def sql_read_gen_info(message):
    sql_info = pd.read_sql('SELECT * FROM patients', sq.connect("patients.db"))
    sql_info.to_excel("gen_info.xlsx")
    with open('gen_info.xlsx', 'rb') as file:
        await bot.send_document(chat_id=message.from_user.id, document=file)


async def sql_read_oms(message):
    sql_info = pd.read_sql('SELECT * FROM quality_oms', sq.connect("quality_oms.db"))
    sql_info.to_excel("oms.xlsx")
    with open('oms.xlsx', 'rb') as file:
        await bot.send_document(chat_id=message.from_user.id, document=file)


async def sql_read_dms(message):
    sql_info = pd.read_sql('SELECT * FROM quality_dms', sq.connect("quality_dms.db"))
    sql_info.to_excel("dms.xlsx")
    with open('dms.xlsx', 'rb') as file:
        await bot.send_document(chat_id=message.from_user.id, document=file)


def check_id(num):
    set_ids = set(ret[0] for ret in cur.execute('SELECT * FROM patients').fetchall())
    return num in set_ids


async def sql_delete_command(data):
    cur.execute('DELETE FROM patients WHERE id == ?', (data,))
    base.commit()

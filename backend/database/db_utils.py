import os
import psycopg2
from dotenv import load_dotenv
from pathlib import Path
from time import sleep


dotenv_path = Path(os.getcwd()) / 'database/docker/.env'
load_dotenv(dotenv_path)

conn = None

def connectDatabase():
    global conn
    try:
        conn = psycopg2.connect(
                host="0.0.0.0",
                port=os.getenv('POSTGRES_PORT'),
                database=os.getenv('POSTGRES_DB'),
                user=os.getenv('POSTGRES_USER'),
                password=os.getenv('POSTGRES_PASSWORD'))
        if conn:
            print('Connected to database')
        else:
            print('Failed to connect to database')
    except Exception as e:
        print(e)
        print('retrying in 5 seconds')
        sleep(5)
        connectDatabase()

def createTables(models):
    cur = conn.cursor()
    for model in models:
        columns = ', '.join([f'{column} {data_type}' for column, data_type in model.columns.items()])
        sqlCommand = f'CREATE TABLE IF NOT EXISTS {model.table_name} ({columns})'
        cur.execute(sqlCommand)
    conn.commit()
    cur.close()

def createElem(model, elem, requiredColumns=None):
    if requiredColumns is None:
        requiredColumns = model.columns.keys()
    for column in model.columns.keys():
        if column == 'id':
            continue
        if column not in requiredColumns:
            continue
        if column not in elem.keys():
            print(f'Column {column} not found in elem')
            return False
    cur = conn.cursor()
    columns = ', '.join([column for column in model.columns.keys() if column != 'id' and column in requiredColumns])
    values = ', '.join([f"'{elem[column]}'" for column in model.columns.keys() if column != 'id' and column in requiredColumns])
    sqlCommand = f'INSERT INTO {model.table_name} ({columns}) VALUES ({values})'
    cur.execute(sqlCommand)
    conn.commit()
    cur.close()
    return True

def deleteTableContent(model):
    cur = conn.cursor()
    sqlCommand = f'DELETE FROM {model.table_name} CASCADE'
    cur.execute(sqlCommand)
    conn.commit()
    cur.close()

def deleteElem(model, details):
    cur = conn.cursor()
    sqlCommand = f'DELETE FROM {model.table_name}'
    for key, value in details.items():
        sqlCommand += f" WHERE {key} = '{value}'"
    cur.execute(sqlCommand)
    conn.commit()
    cur.close()

def getElems(model, details=None):
    cur = conn.cursor()
    sqlCommand = f'SELECT * FROM {model.table_name}'
    if details:
        for key, value in details.items():
            sqlCommand += f" WHERE {key} = '{value}'"
    cur.execute(sqlCommand)
    rows = cur.fetchall()
    cur.close()
    return rows

def modifyElem(model, elemId, modifications):
    cur = conn.cursor()
    sqlCommand = f'UPDATE {model.table_name} SET '
    sqlCommand += ', '.join([f"{key} = '{value}'" for key, value in modifications.items()])
    sqlCommand += f" WHERE id = {elemId}"
    cur.execute(sqlCommand)
    conn.commit()
    cur.close()
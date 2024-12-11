import os
import psycopg2
from dotenv import load_dotenv
from pathlib import Path

dotenv_path = Path(os.getcwd()) / 'database/docker/.env'
load_dotenv(dotenv_path)
# print(os.getcwd())
print(dotenv_path)
print(os.getenv('POSTGRES_DB'), os.getenv('POSTGRES_USER'), os.getenv('POSTGRES_PASSWORD'))

conn = None

def connectDatabase():
    global conn
    try:
        conn = psycopg2.connect(
                host="0.0.0.0",
                database=os.getenv('POSTGRES_DB'),
                user=os.getenv('POSTGRES_USER'),
                password=os.getenv('POSTGRES_PASSWORD'))
    except Exception as e:
        print(e)

def createTables(*models):
    cur = conn.cursor()
    for model in models:
        print(model.columns)
        columns = ', '.join([f'{column} {data_type}' for column, data_type in model.columns.items()])
        sqlCommand = f'CREATE TABLE IF NOT EXISTS {model.table_name} ({columns})'
        cur.execute(sqlCommand)
    conn.commit()
    cur.close()

def createElem(model, elem):
    for column in model.columns.keys():
        if column == 'id':
            continue
        if column not in elem.keys():
            print(f'Column {column} not found in elem')
            return False
    cur = conn.cursor()
    columns = ', '.join([column for column in model.columns.keys() if column != 'id'])
    values = ', '.join([f"'{elem[column]}'" for column in model.columns.keys() if column != 'id'])
    sqlCommand = f'INSERT INTO {model.table_name} ({columns}) VALUES ({values})'
    print(sqlCommand)
    cur.execute(sqlCommand)
    conn.commit()
    cur.close()
    return True
    
    
def getElems(model, details=None):
    cur = conn.cursor()
    sqlCommand = f'SELECT * FROM {model.table_name}'
    if details:
        for key, value in details.items():
            sqlCommand += f" WHERE {key} = '{value}'"
    print(sqlCommand)
    cur.execute(sqlCommand)
    rows = cur.fetchall()
    cur.close()
    return rows
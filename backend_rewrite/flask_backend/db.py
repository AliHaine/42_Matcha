from asyncio import sleep
import psycopg2
import psycopg2.extras
from datetime import datetime

import time

import click
from flask import current_app, g

def get_db():
    if 'db' not in g:
        loop = 0
        while True:
            loop += 1
            try:
                g.db = psycopg2.connect(
                    dbname=current_app.config['DATABASE'],
                    user=current_app.config['DATABASE_USER'],
                    password=current_app.config['DATABASE_PASSWORD'],
                    host=current_app.config['DATABASE_HOST'],
                    port=current_app.config['DATABASE_PORT']
                )
                g.db.cursor_factory = psycopg2.extras.RealDictCursor
                break
            except Exception as e:
                print(f'Error connecting to database (try number : {loop}) : {e}')
                if loop > 10:
                    print('Failed to connect to database after 5 tries, exiting')
                    raise Exception('Failed to connect to database')
                time.sleep(5)
    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()
    with current_app.open_resource('schema_models.sql') as f:
        with db.cursor() as cur:
            cur.execute(f.read().decode('utf8'))
        db.commit()
    with current_app.open_resource('interests_list.txt') as f:
        with db.cursor() as cur:
            category = None
            for line in f:
                line = line.decode('utf-8')
                if len(line.strip()) == 0:
                    continue
                if line.startswith('#'):
                    category = line[1:].strip()
                    continue
                cur.execute('INSERT INTO interests (name, category) VALUES (%s, %s)', (line.strip(), category,))
        db.commit()

@click.command('init-db')
def init_db_command():
    # Clear the existing data and create new tables.
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
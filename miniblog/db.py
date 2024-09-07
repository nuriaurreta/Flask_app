import sqlite3
from flask import current_app, g
import click # se usa para crear interfaces en la línea de comandos

# conectar la base de datos
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3. PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

# cerrar la base de datos
def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

# función para inicializar la base de datos
def init_db():
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

# crea el comando 'init-db' para porder llamarlo desde la línea de comandos
@click.command('init-db')
def init_db_command():
    init_db()
    click.echo('Initialized the database')

# registra las funciones close_db y init_db_command en la instancia de la app
# para que puedan ser llamadas desde __init__
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
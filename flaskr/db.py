import sqlite3

import click
from flask import current_app, g

'''
g:
    特別なオブジェクトで、リクエストごとに個別なものとなる.
    リクエストの処理中は複数の関数によってアクセスされるデータを格納するのに
    使用される.
    connectionは、gオブジェクトに格納されて、もしも同じリクエスの中で get_db が
    2回呼び出された場合、新しいconnectionを作成する代わりに再利用される.
    
current_app:
    特別なオブジェクトで、リクエストを処理中のFlaskアプリケーションを示す.
    get_db()が呼び出されるのは、アプリケーションが作成されてリクエストを
    処理している時であるため、current_appが使用できる.

sqlite3.connect():
    DATABASEで示されるファイルへのconnectionを確立する.
    PARSE_DECLTYPES:
        この定数を設定するとSQLiteのインターフェイスは戻り値のそれぞれのカラムの名前を読み取る.
        "integer primary key"では"integer"が、"number(10)"では"number"が読み取られる.
        URL: https://docs.python.org/ja/3.5/library/sqlite3.html

slite3.Row:
    dictのように振る舞う行を返すようにconnectionへ伝える.
    列名による列へのアクセスを可能にする.
'''
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

'''
connectionが作成済みであるかのチェック
    g.dbが設定されているを調べ、もしconnectionが存在した場合は、それを閉じる.
'''
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

'''
get_db():
    ファイルから読み取ったコマンドを実行するために使用される、データベースのconnectionを返す.
    
open_resourse():
    パッケージflaskrから相対的な場所で指定されたファイルを開く.
'''
def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

'''
click.command():
    init_db()を呼び出して成功時のメッセージを表示する、init-dbと呼ばれる、コマンドラインから
    使用できるコマンドを定義する.
    詳細情報: https://msiz07-flask-docs-ja.readthedocs.io/ja/latest/cli.html
'''
@click.command('init-db')
def init_db_command():
    init_db()
    click.echo('Initialized the database.')

'''
close_db()とinit_db_command()をFlaskアプリケーションのインスタンスに登録
    app.teardown_appcontext():
        レスポンスを返した後のクリーンアップを行なっている時に、close_db()を呼び出すように
        Flaskへ伝える.
    
    app.cli.add_command():
        flaskコマンドを使用して呼び出すことができる新しいコマンドを追加する.
'''
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

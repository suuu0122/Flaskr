import sqlite3

import pytest
from flaskr.db import get_db

'''
test_get_close_db():
    get_db()が常に同じ接続を返すかテストする.
    with app.app_context()ブロックが終了した後は、接続は閉じられているはずである.
'''
def test_get_close_db(app):
    with app.app_context():
        db = get_db()
        assert db is get_db()
    
    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute('SELECT 1')
    
    assert 'closed' in str(e.value)

'''
test_init_db():
    init-dbコマンドを打ち込んだ時に、init_db()が呼び出され、正しく
    メッセージ（Initialized）が出力されるかをテストする.
    
    monkeypatch:
        このテストは、Pytestのfixtureのmonkeypatchを使用して、init_db()を
        それが呼び出された時には記録を残す関数へ置き換える.
    
    runner:
        runner()のfixtureが返すオブジェクトは、init-dbコマンドをコマンド名を
        使用して呼び出すために使用する.
'''
def test_init_db(runner, monkeypatch):
    class Recorder(object):
        called = False
    
    def fake_init_db():
        Recorder.called = True
    
    monkeypatch.setattr('flaskr.db.init_db', fake_init_db)
    result = runner.invoke(args=['init-db'])
    assert 'Initialized' in result.output
    assert Recorder.called

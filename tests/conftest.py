import os
import tempfile

import pytest
from flaskr import create_app
from flaskr.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')

'''
app():
	app()のfixtureでは、factoryを呼び出して、ローカル開発用の設定を使用する代わりに、
    アプリケーションとデータベースをテスト用に設定するtest_configを渡す.
    
    tempfile.mkstemp():
		一時ファイルを作成して開き、そのfileディスクリプタとパスを返す.
        DATABASEのパスは上書きされて、インスタンスフォルダの代わりに、作成した一時ファイルの
        パスを指すようになる.
        パスを設定した後、データベースの表が作成され、テストデータが挿入される.
        テストが終了した後は、一時ファイルが閉じられ削除される.
    
    TESTING:
		appがテストモードであることをFlaskへ伝える.
        Flaskは、テストしやすいように内部的な振る舞いを変更する. その他のFlaskの拡張も自信を
        テストしやすくするために、このTESTINGフラグを使用する可能性がある.
'''
@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()
    
    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
	})
    
    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)
    
    yield app
    
    os.close(db_fd)
    os.unlink(db_path)

'''
client():
	client()のfixtureは、app()のfixtureによって作成されたアプリケーションの
    オブジェクトを使用して、app.test_client()を呼び出す.
    テストでは、このclientを使用してサーバを実行させずに、アプリケーションへの
    リクエストを作成する.
'''
@pytest.fixture
def client(app):
    return app.test_client()

'''
runner():
	runner()のfixtureは、client()のfixtureに似ていて、app.test_cli_runner()は
    アプリケーションに登録されたClickのコマンドを呼び出し可能なrunner(実行者)を作成する.
'''
@pytest.fixture
def runner(app):
    return app.test_cli_runner()

'''
AuthActions:
    大部分のviewでは、ユーザがログインしている必要がある.
    テストの中でログインする最も簡単な方法は、clientを使用してloginのviewへPOST
    リクエストを作成することである.
    ログイン処理を各テストで毎回書くよりも、ログインを行うメソッドを持つクラスを
    書いて、そのクラスへclientを渡すfixtureを各テストで使用する方がよい.
'''
class AuthActions(object):
    def __init__(self, client):
        self._client = client
    
    def login(self, username='test', password='test'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
		)
    
    def logout(self):
        return self._client.get('/auth/logout')

'''
auth():
	auth()のfixtureと合わせると、app()のfixtureの中でテスト用データの一部として
    挿入されたtestユーザとしてログインすることができ、テスト中にauth.login()を
    呼び出せば、ログイン状態にできるようになる.
'''
@pytest.fixture
def auth(client):
    return AuthActions(client)

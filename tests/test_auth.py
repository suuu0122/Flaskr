import pytest
from flask import g, session
from flaskr.db import get_db

'''
test_register():
    ページが上手く表示されるかをテストする.
    単純なリクエストを作成し、200 OKのステータスコードが返ってくるかをチェックする.
    表示が失敗した場合は、500 Internal Server Errorのステータスコードが返ってくる.
    
    client.get():
        GETリクエスト作成して、Flaskによって返されたResposeオブジェクトを返す.
    
    client.post():
        POSTリクエストを作成して、dataのdictをformのデータへ変換する.
    
    headers:
        registerのviewがログインのviewへリダイレクトした時、ログインのURLに設定された
        Locationへのヘッダを持つ.
'''
def test_register(client, app):
    assert client.get('/auth/register').status_code == 200
    response = client.post(
        '/auth/register', data={'username': 'a', 'password': 'a'}
	)
    assert response.headers["Location"] == "/auth/login"
    
    with app.app_context():
        assert get_db().execute(
            "SELECT * FROM user WHERE username = 'a'",
		).fetchone() is not None

'''
pytest.mark.parametrize:
    同じテスト用関数を違う引数で走らせるようにPytestに伝える.
    ここでは、異なる不正な入力とエラーメッセージを、3回同じコードを書くことなく、テスト
    するために使用している.

test_register_validate_input():
	data:
        レスポンスの本体（body）をバイト（bytes）として含む.
        もしある値をページ上に表示することを期待する場合、それがdataの中に存在するかを
        チェックする. bytes型はbytes型と比較しなければならない.
        もしテキストを比較したい場合は、get_data(as_text=True)を代わりに使用する.
'''
@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('', '', b'Username is required.'),
    ('a', '', b'Password is required.'),
    ('test', 'test', b'already registerd.'),
))
def test_register_validate_input(client, username, password, message):
    response = client.post(
        '/auth/register',
        data={'username': username, 'password': password}
	)
    assert message in response.data

'''
test_login():
	loginのviewのテストは、test_register()と非常に似ており、registerのように
    データベースの中のデータをテストするのではなく、sessionがログイン後にはuser_id
    を持っているかをテストする.
    
    with client:
        clientをwithブロックの中で使用すると、レスポンスが返された後にsessionの
        ようなcontextの変数（リクエストの処理中だけ設定されている変数）へアクセス
        できる.
        通常は、sessionへリクエストの外側からアクセスしようとするとエラーを引き起こす.
'''
def test_login(client, auth):
    assert client.get('/auth/login').status_code == 200
    response = auth.login()
    assert response.headers["Location"] == "/"
    
    with client:
        client.get('/')
        assert session['user_id'] == 1
        assert g.user['username'] == 'test'

'''
test_logout():
    ログアウトは、sessionはログアウトした後にuser_idを含んでいないかをテストする.
'''
def test_logout(client, auth):
    auth.login()
    
    with client:
        auth.logout()
        assert 'user_id' not in session

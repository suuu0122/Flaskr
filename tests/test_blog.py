import pytest
from flaskr.db import get_db

'''
ブログ:
    すべてのブログのviewは、conftest.pyで書いたauthのfixtureを使用する.
    auth.login()を呼び出すと、それ以降のクライアントからのリクエストは、testユーザ
    としてログインされたものなる
'''

'''
test_index():
    indexのviewは、テストデータを使用して追加された投稿記事についての情報を表示するを
    テストする.
    ログインしていない場合は、各ページはログインまたは登録へのリンクを表示するはずである.
    作者としてログインした場合は、投稿記事を編集できるリンクが存在するはずである.
    ログインしていた場合は、ログアウトへのリンクがあるはずである.
'''
def test_index(client, auth):
    response = client.get('/')
    assert b"Log In" in response.data
    assert b"Register" in response.data

    auth.login()
    response = client.get('/')
    assert b'Log Out' in response.data
    assert b'test title' in response.data
    assert b'by test on 2018-01-01' in response.data
    assert b'test\nbody' in response.data
    assert b'href="/1/update"' in response.data


'''
test_login_required():
    ログインしていない場合は、create、update、deleteのviewへアクセスできないことを
    テストする（ログインのviewへリダイレクトされる）.
'''
@pytest.mark.parametrize('path', (
    '/create',
    '/1/update',
    '/1/delete',
))
def test_login_required(client, path):
    response = client.post(path)
    assert response.headers["Location"] == "/auth/login"

'''
test_author_required():
    ログインしているユーザが作者でない場合は、投稿記事のupdate、deleteへはアクセス
    できないことをテストする（403 Forbidden）.
'''
def test_author_required(app, client, auth):
    # 作者から他のユーザへチェンジ
    with app.app_context():
        db = get_db()
        db.execute('UPDATE post SET author_id = 2 WHERE id = 1')
        db.commit()
    
    auth.login()
    # 現在のユーザは、他のユーザの投稿を変更不可
    assert client.post('/1/update').status_code == 403
    assert client.post('/1/delete').status_code == 403
    # 現在のユーザは、編集リンクを見れない
    assert b'href="/1/update"' not in client.get('/').data

'''
test_exists_required():
    与えられたidのpost（投稿記事）が存在しない場合は、update、deleteにアクセスすると
    何も見つからないことをテストする（404 Not Found）.
'''
@pytest.mark.parametrize('path', (
    '/2/update',
    '/2/delete',
))
def test_exists_required(client, auth, path):
    auth.login()
    assert client.post(path).status_code == 404

'''
test_create():
    投稿記事がcreateできるかをテストする.
    createのviewはGETリクエストに対して200 OKのステータスコードを返すはずである.
    正しいデータがPOSTリクエストとして送られてきた時は、createは新しい投稿記事の
    データをデータベースへ挿入するはずである. -> 投稿記事数が1から2へ増える.
'''
def test_create(client, auth, app):
    auth.login()
    assert client.get('/create').status_code == 200
    client.post('/create', data={'title': 'created', 'body': ''})
    
    with app.app_context():
        db = get_db()
        count = db.execute('SELECT COUNT(id) FROM post').fetchone()[0]
        assert count == 2

'''
test_update():
    投稿記事がupdateできるかをテストする.
    updateのviewはGETリクエストに対して200 OKのステータスコードを返すはずである.
    正しいデータがPOSTリクエストとして送られてきた時は、updateは編集された投稿記事の
    データをデータベースへ挿入するはずである. -> 投稿記事のタイトルが編集後のタイトルに変化する.
'''
def test_update(client, auth, app):
    auth.login()
    assert client.get('/1/update').status_code == 200
    client.post('/1/update', data={'title': 'update', 'body': ''})
    
    with app.app_context():
        db = get_db()
        post = db.execute('SELECT * FROM post WHERE id = 1').fetchone()
        assert post['title'] == 'update'

'''
test_create_update_validate():
    不正なデータがPOSTリクエストとして送られてきた時に、create、updateのviewが
    エラーメッセージを表示するかをテストする.
'''
@pytest.mark.parametrize('path', (
    '/create',
    '/1/update',
))
def test_create_update_validate(client, auth, path):
    auth.login()
    response = client.post(path, data={'title': '', 'body': ''})
    assert b'Title is required.' in response.data

'''
test_delete():
    投稿記事を削除した時に、indexのviewへリダイレクトされ、投稿記事は存在しなく
    なっているかをテストする.
'''
def test_delete(client, auth, app):
    auth.login()
    response = client.post('/1/delete')
    assert response.headers["Location"] == "/"
    
    with app.app_context():
        db = get_db()
        post = db.execute('SELECT * FROM post WHERE id = 1').fetchone()
        assert post is None

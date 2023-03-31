from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('blog', __name__)

'''
インデックス:
    インデックスは、最新の投稿記事を最初にして、投稿記事をすべて表示する.
    結果の中でuserテーブルから作者情報を使用するために、SQL文の中でJOINを使用している.
'''
@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/index.html', posts=posts)

'''
作成:
    createのviewは、authのregisterのviewと同じように機能する.
    formが表示されるか、postされたデータが検証されてから、データベースへその投稿記事が追加されるか、
    エラーが表示される.
'''
@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None
        
        if not title:
            error = 'Title is required.'
        
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES(?, ?, ?)',
                (title, body, g.user['id'])
			)
            db.commit()
            return redirect(url_for('blog.index'))
    
    return render_template('blog/create.html')

'''
更新:
    updateとdeleteのviewは両方とも、idを使用してpost（投稿記事）を取得し、ログインしているユーザが
    作者と一致しているかをチェックする必要がある.
    コードの重複を避けるために、postを取得する関数を書いて、各viewから呼び出すことが可能である.
    
    get_post():
        check_author引数を定義するのは、作者をチェックせずにpostを取得する時に、この関数を使用可能に
        するためである. これは、個々のpostをページ上に表示する、postの変更はしないためユーザが誰であっても
        問題ないページのviewを書く場合に便利である.
    
    update():
        id引数を受け取り、それはrouteの中にある<int:id>部分に対応する.
        実際のURLは、/1/updateのようになる. Flaskは1を捉えて、それがintであることを確認し、それをid引数
        として渡す. もし、int:を指定せず代わりに<id>を使用した場合は、文字列になる.
'''
def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
	).fetchone()
    
    if post is None:
        '''
        abort():
            HTTPのステータスコードを返す特殊な例外を発生させる.
            エラーと一緒に表示されるメッセージをオプションで受け取り、メッセージがない場合は
            標準設定のメッセージを返す（404の場合はNot Found）.
        '''
        abort(404, f"Post id {id} doesn't exits.")
        
    if check_author and post['author_id'] != g.user['id']:
        abort(403)
    
    return post

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)
    
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None
        
        if not title:
            error = 'Title is required.'
        
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
			)
            db.commit()
            return redirect(url_for('blog.index'))
        
    return render_template('blog/update.html', post=post)

'''
削除:
    deleteのviewは、自身のテンプレートを持たず、削除ボタンはupdate.htmlの一部になって、
    /<id>/deleteのURLへpostする.
    テンプレートがないため、それはPOSTメソッドだけを処理して（GETは必要ない）、indexのviewへリダイレクトする.
'''
@bp.route('/<int:id>/delete', methods=('POST', ))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))

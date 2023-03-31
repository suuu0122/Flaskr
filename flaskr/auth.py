import functools

'''
Blueprint:
    関連するviewおよびその他のコードをグループへと編成する方法.
    viewおよびその他のコードを直接Flaskアプリケーションに登録する代わりに、
    それらをblueprintに登録する.
    Flaskアプリケーションが利用可能になった時に、blueprintをFlaskアプリケーションに
    登録する.
    Flaskでは2つのblueprintがあり、1つは認証に関する関数のためであり、もう1つはブログへの
    投稿記事に関する関数のためである.

view:
    viewの関数は、アプリケーションへのリクエストに対して応答するために書くコード.
    Flaskは受信するリクエストのURLを、それを処理すべきviewへと照合するために、
    URLのパターンを使用する.
    送信用のレスポンスへとFlaskが変換するデータをviewは返す.
'''
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

'''
Blueprint():
    auth:
        authと名付けられたBlueprintを作成する.
    __name__:
        blueprintは、Flaskアプリケーションのオブジェクトと同様に、自分がどこで定義されているかを
        知る必要があるので、__name__が引数として渡される.
    url_prefix:
        blueprintと関連づけられているすべてのURLのパス部分の先頭に付けられる.
'''
bp = Blueprint('auth', __name__, url_prefix='/auth')

'''
最初のview登録
    ユーザが /auth/register のURLを訪れた時は、registerのviewはユーザが記入すべき
    formを持つHTMLを返す.
    ユーザの入力を検証し、エラーメッセージと一緒にformを再表示するか、新しいユーザを
    作成してログインページへ行くようにする.
    
    @bp.route:
        URLの/registerとregisterのview関数を関連付ける.
        Flaskが /auth/register へのリクエスト受信した時、Flaskはregisterの
        viewを呼び出し、その戻り値をレスポンスとして使用する.
    
    if request.method == 'POST':
        ユーザがformを提出した時、Request.methodはPOSTになる.
        POSTの場合は、入力データの検証を行う.
    
    request.form:
        提出されたformのキーと値を対応付ける、dictの特別なタイプ.
        ユーザは自分のusernameとpasswordを入力する.
    
    db.execute():
        エスケープ処理:
            SQLインジェクション攻撃に対して脆弱にならないように値のエスケープをする.
            URL: https://petitviolet.hatenablog.com/entry/20120531/1338429793
        generate_password_hash():
            セキュリティのためにパスワードは決してデータベースへ直接格納してはいけない.
            generate_password_hash()を使用してパスワードを安全にハッシュし、そのハッシュを
            格納する.
        db.commit():
            db.execute()内のこのクエリは、データを変更するのでdb.commit()を呼び出す必要がある.
    
    db.IntegrityError:
        usernameが既に存在している場合、sqlite3.IntegrityErrorが起こるので対応.
        詳細情報: https://docs.python.org/3/library/sqlite3.html#sqlite3.IntegrityError
    
    url_for():
        ユーザ情報を格納した後、ログインページへリダイレクトする.
        url_for()は、ログインのviewの関数の名前から対応するURLを生成する.
        URLにリンクしているすべてのコードを変更させずに済ますことができるので、URLをハードコーディング
        するよりも好ましい方法である.
    
    redirect():
        生成されたURLへリダイレクトさせるレスポンスを生成する.
    
    flash():
        テンプレートを変換（render）する時に取得可能なメッセージを格納する.
        フラッシュメッセージは、ユーザが何らかの行動を起こした時に、その行動が正しく処理されたことを
        知らせたり、失敗したことを知らせるために利用される.
        参考: https://qiita.com/kotmats/items/fcff19ae5ea309d9fee9
        詳細情報: https://msiz07-flask-docs-ja.readthedocs.io/ja/latest/patterns/flashing.html
    
    render_template():
        登録formのあるHTMLを含んだテンプレートを変換する.
        テンプレートを表示するのにrender_template()を使用し、テンプレートのHTMLファイルはデフォルトで
        アプリケーションのpythonファイルと同じ階層のtemplatesフォルダに配置する.
        参考: https://www.nblog09.com/w/2020/12/11/flask-templte/
'''
@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        
        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
				)
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registerd."
            else:
                return redirect(url_for("auth.login"))
        
        flash(error)
    
    return render_template('auth/register.html')

'''
ログイン
    fetchone():
        queryの結果から1行を返す.
        queryが何も結果を返さない場合は、Noneを返す.

    check_password_hash():
        submitさらたパスワードを、格納されたハッシュと同じ方法でハッシュし、セキュリティに
        注意しながらそれらを比較する.
        比較結果が一致した場合、パスワードは適正である.

    session:
        リクエストをまたいで格納されるデータのdict.
        ユーザのidは新しいsessionに格納される. そのデータはブラウザへ送信されるcookieに格納され、
        ブラウザは以降のリクエストでcookieを送信し返す.
        Flaskは、データを改竄されないようにするため、安全にデータを署名する.
    
    ログイン処理後は、ユーザのidはsessionへ格納され、以降のリクエストで利用可能になる.
'''
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

'''
bp.before_app_request():
    どのURLにリクエストされたかに関わらず、viewの関数の前に実行する関数を登録する.

load_logged_in_user():
    ユーザidがsessionに格納されているかチェックした後、データベースからユーザのデータを取得し、
    そのデータをリクエストの期間中は存続するg.userへ格納する.
    もしユーザidがsessionにない場合、もしくはそのユーザidがデータベースに存在しない場合、
    g.userはNoneになる.
'''
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('usr_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

'''
ログアウト:
    ユーザidをsessionから取り除く.
    そうすることで、load_logged_in_user()は以降のリクエストでユーザ情報を読み込まなくなる.
'''
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

'''
他のviewでの認証の要求
    ブログの投稿記事を作成、編集、削除するにはユーザがログインしている必要がある.
    デコレータを使用すると、decoratorを適用した各viewでログインをチェックできる.

    login_required():
        このデコレータは、適用した元のviewの関数をラップする新しいviewの関数を返す.
        その新しい関数はユーザ情報が読み込まれているかをチェックして、読み込まれていない場合は
        ログインページへリダイレクトする.
        ユーザ情報が読み込まれている場合は、元のviewが呼び出されて通常通りに続ける.
'''
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    
    return wrapped_view

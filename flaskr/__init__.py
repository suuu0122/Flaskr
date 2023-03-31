import os

from flask import Flask

def create_app(test_config=None):
    '''
    Flaskインスタンスの作成
        __name__: 
            この時点でのPythonのモジュール名. 
            appはいくつかのpathを用意するので、appがどの場所にあるか知る必要があり、
            __name__はそれを伝えるのに便利な方法.
        
        instance_relative_config=True:
            設定ファイルの場所がインスタンスフォルダから相対的に示されることをappへ伝える.
            インスタンスフォルダは、flaskrパッケージの外側に存在し、秘密情報の設定やデータベースのファイルなど、
            バージョン管理へコミットするべきではないローカルのデータを保持することができる.
    '''
    app = Flask(__name__, instance_relative_config=True)
    
    '''
    appが使用する標準設定の設定
        SECRET_KEY:
            データを安全に保つためにFlaskとFlask拡張によって使用される.
            開発中は便利な値を提供するために、ここでは'dev'に設定されているが、
            デプロイをする時には無作為な値（random value）で上書きするべきである.
        DATABASE:
            SQLiteデータベースファイルが保存されるパス.
            Flaskがインスタンスフォルダに選んだパスである app.instance_path の下になる.
    '''
    app.config.from_mapping(
        SECRET_KEY = 'dev',
        DATABASE = os.path.join(app.instance_path, 'flaskr.splite'),
	)
    
    if test_config is None:
        '''
        config:
            インスタンスフォルダに config.py が存在する場合、値をそのファイルから取り出して、
            標準設定を上書きする.
            デプロイの時には、本当のSECRET_KEYを設定するために使用できる.
        
        silent:
            デフォルトではFalseであり、Trueにすると、ファイルや環境変数が見つからなかった場合に、
            例外を発生させるのではなく、Falseを返すようになる.
            URL: https://www.subarunari.com/entry/2018/03/17/%E3%81%84%E3%81%BE%E3%81%95%E3%82%89%E3%81%AA%E3%81%8C%E3%82%89_Flask_%E3%81%AB%E3%81%A4%E3%81%84%E3%81%A6%E3%81%BE%E3%81%A8%E3%82%81%E3%82%8B_%E3%80%9CConfiguration%E3%80%9C
        '''
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
    
    try:
        '''
        os.makedirs()は、app.instance_pathが確実に存在するようにする.
        Flaskはインスタンスフォルダを自動的に作成しないが、このプロジェクトではそこに
        SQLiteデータベースファイルを作成するのでインスタンスフォルダが確実に作成されている必要がある.
        '''
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    '''
    init_app()の呼び出し
    '''
    from . import db
    db.init_app(app)

    '''
    blueprintをimportして登録
        この認証のblueprintは、新しいユーザ登録と、ログイン/ログアウトのviewを持つようにする.
    '''
    from . import auth
    app.register_blueprint(auth.bp)

    '''
    blueprintをimportして登録
        blogのblueprintは、authと異なりurl_prefixを持たない.
        -> indexのviewの場所（URL）は/、createのviewの場所（URL）は/createのようになる.
        add_url_rule():
            url_for('index')またはurl_for('blog.index')のどちらも機能し、いずれも同一の/をURLとして
            生成するように、エンドポイント名'index'をURLの/と関連付ける.
    '''
    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')
    
    return app

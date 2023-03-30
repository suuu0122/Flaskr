# Flaskr

## [Flaskとは](https://aiacademy.jp/media/?p=57)
* Flaskは、PythonのWebアプリケーションフレームワークの1つ.
* 小規模向けの簡単なWebアプリケーションを作成するのに適している.
* Webフレームワークは、ウェブサイトやウェブアプリケーションを作成するための機能を提供し、容易にWebアプリケーションを作成することができる.
* Pythonには、Flask以外にもWebアプリケーションフレームワークがあり、Django、Fast、pyramid、bottleなどがある.
* Flaskのインストール手順
	* チュートリアルでは、仮想環境を構築し、その中にFlaskをインストールすることが推奨されている.
	* [仮想環境の構築](https://msiz07-flask-docs-ja.readthedocs.io/ja/latest/installation.html)
		```zsh
		mkdir [directory_name]
		cd [directory_name]
		python3 -m venv [virtual_environment_name]
		```
	* 仮想環境の有効化
		```zsh
		. [virtual_environment_name]/bin/activate
		```
	* Flaskのインストール
		```zsh
		pip install Flask
		```
* アプリケーションの実行
	```zsh
	flask --app [directory_name] --debug run
	```
	* デバッグモードは、ページが例外を起こした時はいつでもインタラクティブなデバッガを表示し、コードを変更した時にはサーバを再起動する.
	* チュートリアルを進める時は、Flaskを実行させたままにしながら、ブラウザのページを再読み込みするだけでよい.
	* アプリケーションをストップさせるには、`Ctrl + C`を押す.
<br />

## [`__init__.py`とは](https://qiita.com/msi/items/d91ea3900373ff8b09d7)
* [モジュールとパッケージ](https://rinatz.github.io/python-book/ch04-02-packages/)
	* モジュールとパッケージの関係は、ファイルシステムでのファイルとディレクトリの関係に一致する.
	* モジュールを使用することで関数やクラスをまとめることができるが、1つのモジュール内に多くの定義を含めてしまうとコードが長くなり分かりにくくなる.<br>
	-> ファイルを分割して複数のモジュールを作成し、それを1つのディレクトリに集約する.<br>
	-> 複数のモジュールを集約したディレクトリのことを **パッケージ** と呼ぶ.
* `__init__.py`の役割
	* 下記のような階層構造を考える.
		```zsh
		./
		|-sample0020.py ...実行ファイル
		|-dir/
		   |-module02.py ...モジュール
		```
		* `dir/module02.py`
			```python
			def hello():
				print("Hello, world! from module02")
			```
		* `sample0020.py`から`module02`を呼び出すには次のように記述する必要がある.
			```python
			import dir.module02
			dir.module02.hello()
			```
	* `module02`を呼び出すのに、`dir/`というディレクトリがあるために、`dir.module02`という名前空間で参照する必要があり、`dir`には実体がないのに、名前空間の階層として指定しなくてはならず面倒.<br>
	-> `__init__.py`を作成することで、直接`module02`を呼び出すことができる.
	* 下記のように階層構造を書き換えることで、直接`module02`を呼び出すことができる.
		```zsh
		./
		|-sample0030.py ...実行ファイル
		|-module02/
		   |-__init__.py ..."module02"の実体
		```
		* `module02/__init__.py`
			```python
			def hello():
				print("Hello, world! from __init__.py")
			```
		* `sample0030.py`
			```python
			import module02
			module02.hello()
			```
	* ファイルとして存在するモジュールのクラス（名前空間）では、`__init__()`を記載する場所があるが、ディレクトリとして存在する名前空間には`__init__()`を書く場所がないため、その代わりとして`__init__.py`というファイルを作成するようにした.
	* `__init__.py`は、ディレクトリ名をモジュール名としてマッピングするためのファイルと言える.
<br />

## SQLite
* [SQLiteとは](https://products.sint.co.jp/topsic/blog/sqlite)
	* SQLiteは、オープンソースで軽量のRDBMS（データベース管理システム）.
	* 簡易的な（ライトな）データベースであり、サーバとしてではなく、アプリケーションに組み込むことで効果を発揮する.
	* MySQLやPostgresqlなどの主要なデータベースは、データベース用のサーバが必要になることが多いが、SQLiteは1つのファイルでデータベースを管理するので非常に扱い易い.
	* いわゆる「組み込み型RDBMS」な特徴からスマホアプリ内の設定情報などをアプリ内部で格納しておけるので、近年非常によく使われるRDBMSとなっている.
	* SQLiteの3つの特徴
		* 設定不要な自己完結型システム
			* SQLiteは、設定不要で利用することができる. 他のデータベースであれば、設定ファイルを用意して、プロセスの起動や停止、データベースインスタンスの設定が必要.
			* SQLiteは、サーバプロセスではなく、ライブラリとして使用できるため、設定が不要.
		* マルチプラットフォーム
			* Linux、Solaris、Windows、Mac、Android、iOSなどに対応.
		* データ型の指定を強制しない
			* SQLiteは、データ型を指定せずともテーブルの作成が可能. 通常のデータベースでは、テーブルの絡むごとに「文字列型」「数値型」といったデータ型を明確に定義し、指定外のデータは格納できない.
			* SQLiteは、データ型を指定することも可能であり、指定しない場合でも格納されたデータによってデータ型を自動的に判別している.
* [PythonでのSQLite操作](https://products.sint.co.jp/topsic/blog/how-to-use-sqlite-in-python)
	* sqlite3モジュールをインポート
		* Pythonでsqliteを使用するには、「sqlite3」モジュールをimportして使用するのがよい. 
		* 組み込みモジュールなので、pip等でインストールする必要はない.
		```python
		import sqlite3
		```
	* データベース作成
		```python
		import sqlite3

		dbname = 'main.db'

		# DBを作成（既に作成されている場合はこのDBに接続）
		conn = sqlite3.connect(dbname)

		# DBとの接続を閉じる（必須）
		conn.close()
		```
		* データベースが作成されると、実行ファイルと同じ階層に`dbname`で指定したファイルが作成される.
	* テーブル作成
		```python
		import sqlite3

		dbname = 'main.db'
		conn = sqlite3.connect(dbname)

		# SQLiteを操作するためのカーソルを作成
		cur = conn.cursor()

		# テーブルの作成
		cur.execute(
			'CREATE TABLE items(id INTEGER PRIMARY KEY AUTOINCREMENT, name STRING, price INTEGER)'
		)

		conn.close
		```
		* `execute()`にCREATE TABLE文を渡してテーブルを作成する.
		* `execute()`にSQL文を渡すことで、どんなSQLも実行可能.
	* テーブルにデータを登録
		```python
		import sqlite3

		dbname = 'main.db'
		conn = sqlite3.connect(dbname)

		# SQLiteを操作するためのカーソルを作成
		cur = conn.cursor()

		# データ登録
		cur.execute('INSERT INTO items values(0, "りんご", 100)')

		# コミットしないと登録が反映されない
		conn.commit()

		conn.close
		```
		* データを複数件登録するには、`executemany()`を使用する.
			```python
			# 登録するデータ
			inserts = [
				(1, "みかん", 80),
				(2, "ぶどう", 150),
				(3, "バナナ", 60)
			]

			# 複数データ登録
			cur.executemany('INSERT INTO items values(?,?,?)', inserts)
			```
	* テーブルのデータ取得
		```python
		import sqlite3

		dbname = 'main.db'
		conn = sqlite3.connect(dbname)

		# SQLiteを操作するためのカーソルを作成
		cur = conn.cursor()

		# データ検索
		cur.execute('SELECT * FROM items')

		# 取得したデータはカーソルの中に入る
		for row in cur:
			print(row)
			'''
			(0, 'りんご', 100)
			(1, 'みかん', 80)
			(2, 'ぶどう', 150)
			(3, 'バナナ', 60)
			'''
		
		conn.close()
		```
	* テーブルデータの更新・削除
		```python
		import sqlite3

		dbname = 'main.db'
		conn = sqlite3.connect(dbname)

		# SQLiteを操作するためのカーソルを作成
		cur = conn.cursor()

		# データ更新
		cur.execute('UPDATE items SET price=260 WHERE id="3"')

		# データ削除
		cur.execute('DELETE FROM items WHERE id="2"')

		cur.execute('SELECT * FROM items')
		for row in cur:
			print(row)
			'''
			(0, 'りんご', 100)
			(1, 'みかん', 80)
			(3, 'バナナ', 260)
			'''
		
		conn.close()
		```
<br />

## [SQLインジェクション](https://www.softbanktech.co.jp/special/blog/it-keyword/2021/0020/)
* SQLインジェクションとは
	* SQLインジェクションとは、SQLのデータベースに不正なプログラムを注入、挿入するサーバ攻撃の総称.
	* SQLインジェクションにより、情報漏洩や消去、改ざん、悪用されるといった被害を受ける可能性がある.
* SQLインジェクションとクロスサイトスクリプティングの違い
	* クロスサイトスクリプティングは、脆弱性のあるウェブサイトに対して攻撃を行い、ユーザの個人情報やパソコンそのものを乗っ取る手法.
	* ウェブサイトの脆弱性を狙う点では同じであるが、SQLインジェクションの場合はSQLによるデータサーバを使用する点で異なる.
* SQLインジェクションの仕組み
	* 攻撃者がSQLサーバを操作する命令文を作成する.
	* Webサイトは、ユーザIDやパスワードを入力すると不正な文字列が入力されていないかのチェックを行う. 入力エリアに脆弱性があると、SQL文を含ませた文字列を入力され、不正なSQLが実行される.
* SQLインジェクション対策
	* エスケープ処理を行う.
		* SQLインジェクション対策として最も効果的な方法.
		* エスケープ処理とは、プログラム言語で使用される特別な文字や記号をルールに沿って、別の文字列に書き換えることである.
		* SQLインジェクション対策の場合は、セミコロン（;）やシングルクォート（'）などの記号が対象となる. これらの特殊文字を普通の文字として認識するように設定することで、攻撃者が仮に不正なSQLを送り込んできたとしてもそれを無効化できる.
	* 想定している文字以外を使用しない.
		* SQLインジェクションは特殊文字を使用しないと攻撃ないため、半角数字の入力以外を入力禁止にする.
		* 想定している文字以外は使用しない方法にPODを使用するという方法もある.
	* データベースサーバのログを監視、解析する.
	* セキュリティソフトを導入する.
* [python-sqlite3でのエスケープ処理](https://petitviolet.hatenablog.com/entry/20120531/1338429793)
<br />

## [CookieとSession](https://www.engilaboo.com/definitely-understand-cookie-session/)
* Cookieとは
	* データをブラウザに保存する仕組み.
* Sessionとは
	* ユーザが行う一連の動作（ログイン〜ログアウト）
* CookieとSessionを使用する意味
	* Cookieを使用してSession管理することで、HTTP通信の「ステートレス」という性質を克服して、状態を保持できるようになる（擬似的にステートフルにすることができる）.
* ステートレスとは
	* サーバがクライアントの情報を保持し続けられない.<br>
	-> サーバ側が同一クライアントからのアクセスか否かを判定できない.
	* 例としてショッピングサイトでの買い物を考えると、リクエストの度に状態がリセットされるため、アクセスの度に買い物カゴがリセットされ、「買い物カゴ」という機能自体を作成することができない.<br>
	-> CookieとSessionが必要！
* CookieとSessionで状態を保持する仕組み
	* ユーザがショッピングサイトにアクセス.
	* ショッピングサイトのサーバは「SessionID」を生成して、ユーザと紐付けた上でサーバに保存.
	* ショッピングサイトの画面を返すと同時に、このSessionIDをブラウザに渡す.
	* ブラウザは、この送られてきたSessionIDを、送り元のサーバの情報を含めた上で、「Cookie」に保存.

		![Cookie_Session_image](img/cookie_session_image.png)
	
	* ユーザは次の商品を買い物カゴに入れるために、ショッピングサイトのサーバにリクエストを送信（このとき、Cookieに紐付いているサーバ情報をもとに、先ほどCookieにセットしたSessionIDが自動的にサーバに送信される）.
	* サーバはSessionIDにより「誰からの通信か」を認識した上で、選択された商品をSessionIDと紐付けてサーバ側のデータベースに保存（Session情報はデータベースだけでなく場所に保存可能）.
<br />

## [デコレータ](https://qiita.com/mtb_beta/items/d257519b018b8cd0cc2e)
* デコレータとは
	* デコレーターを利用することで、既存関数の処理の前後に自分自身で、処理を付け加えることができる.
	* デコレーターを使うことで、ライブラリとして提供されている関数を呼んだときに自動的に実行される処理を付加できる.
	* Pythonでは、Javaなどで利用されるオーバーライドのような形で関数自体を書き換えてしまうことも可能ではある. しかしながら、既存の処理には問題はないが、違う処理も同時にさせたい状況などでデコレータを使用する.
	* 今回のFlaskのチュートリアルでは、関数を実行する前にユーザ情報が読み込まれているかをチェックしたいのでデコレータを使用する.
* デコレータの実装例
	```python
	def deco(func):
		def wrapper(*args, **kwargs):
			print('--start--')
			func(*args, **kwargs)
			print('--end--')
		return wrapper
	
	@deco
	def test():
		print('Hello Decorator')
		
	test()

	# --start--
	# Hello Decorator
	# --end--
	```
* [`*args`と`**kwargs`](https://note.nkmk.me/python-args-kwargs-usage/)
	* 関数定義で引数に`*`と`**`（1個または2個のアスタリスク）を付けると、任意の数の引数（可変長引数）を指定できる.
	* 慣例として`*args`、`**kwargs`という名前が使用されることが多いが、`*`と`**`が頭についていれば他の名前でも問題ない.
	* `*args`: 複数の引数をタプルとして受け取る.
	* `**kwargs`: 複数のキーワード引数を辞書として受け取る.
<br />

## [エンドポイントとURL](https://msiz07-flask-docs-ja.readthedocs.io/ja/latest/tutorial/views.html)
* `url_for()`は、viewの名前と引数に基づいて対応するURLを生成する.
* viewに関連付けられた名前は **エンドポイント** とも呼ばれ、標準設定ではviewの関数の名前と同じになる.
* エンドポイントは、view用の関数などを特定するもので、Flask実装上はdictionaryである **view_functions** 属性のキーになる.
* Flask実装では、アプリケーションが使用するview用の関数などはすべてview_functions属性に、エンドポイントをキーに関数本体を値にして登録される.
* 多くの場合、関数名とエンドポイントは同じであるが、異なる値がエンドポイントになる場合もある.
* Flaskでは`route()`デコレータを使用すると内部的にWerkzeugのRuleインスタンスを作成して、URLのパターンとエンドポイントを対応付ける.
* 例えば、チュートリアルの最初でapp factoryに追加されたviewの`hello()`は、名前（エンドポイントを特に指定しなければ関数名と同じ）が`'hello'`であり、`url_for('hello')`を使用してリンクすることができた. 
* もし引数を取る場合は、`url_for('hello', who='World')`のようにしてリンクすることができる.
* blueprintを使用する時は、blueprintの名前が関数名の前に付けられるので、`login()`のエンドポイントは、blueprintの`'auth'`に`login()`関数を追加しているため`'auth.login'`になる.
<br />

## [テンプレート](https://msiz07-flask-docs-ja.readthedocs.io/ja/latest/tutorial/templates.html)
* テンプレートファイルは、flaskrパッケージ内のtemplatesディレクトリに格納する.
* テンプレートファイルとは、静的データと動的データのためのプレースホルダを含んでいるファイルである.
* テンプレートは、最終ドキュメントを作成するために特定のデータと一緒に変換（render）される.
* Flaskは、テンプレートの変換（render）にテンプレートライブラリのJinjaを使用する.
* Flaskでは、HTMLテンプレートの中で変換されるあらゆるデータを自動エスケープするようにJinjaが設定されている.<br>
-> ユーザが入力したデータを安全に表示できる（`<`や`>`のようなHTMLに干渉しかねない文字が入力されても、ブラウザの中では同じように見える安全な値へエスケープする）.
* ベースのテンプレートは、templatesディレクトリに直接置かれるが、blueprintのテンプレートは、templates下のblueprintと同じ名前のディレクトリに置かれる.
<br />

## [Jinja](https://shigeblog221.com/python-flask3/)
* Jinjaは、python用テンプレートエンジンの1つ.
* テンプレートエンジンは、ユーザの操作に合わせて、HTMLの内容を部分的に適した内容に書き換える仕組みで、テンプレートと呼ばれる雛形と、あるデータモデルで表現される入力データを合成し、ドキュメントを出力するソフトウェアである.
* Flaskをインストールすると、Jinja2も同時にインストールされる.
* [jinjaの使い方](https://www.sukerou.com/2019/04/jinja2flaskjinja2.html)
<br />

## [静的ファイル](https://msiz07-flask-docs-ja.readthedocs.io/ja/latest/tutorial/static.html)
* HTMLレイアウトにスタイルを加えるために、CSSを追加することができる. スタイルは変化しないので、テンプレートファイルではなく、静的（static）ファイルになる.
* Flaskは、flaskr/staticディレクトリからの相対パスに対応するファイルのviewを自動的に追加する.
* CSSに加えて、他の種類の静的ファイルにロゴ画像やJavaScript関数のファイルがある場合、それらはすべてflaskr/staticディレクトリの下に置き、`url_for('staic', filename='...')`により参照できる.
<br />

## Reference
* [Tutorial](https://msiz07-flask-docs-ja.readthedocs.io/ja/latest/tutorial/index.html)
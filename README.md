# Flaskr

## Index
* [Flaskとは](#about-Flask)
* [`__init__.py`とは](#about-init.py)
* [SQLite](#SQLite)
* [SQLインジェクション](#sql-injection)
* [CookieとSession](#cookie-and-session)
* [デコレータ](#decorator)
* [エンドポイントとURL](#endpoint-and-url)
* [テンプレート](#template)
* [Jinja](#jinja)
* [静的ファイル](#static-file)
* [プロジェクトをインストール可能にする](#can-install-project)
* [プロジェクトのインストール](#install-project)
* [テストの網羅率](#test)
* [本番環境へのデプロイ](#deploy)
* [Reference](#reference)
<br />

<a id="about-Flask"></a>

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

<a id="about-init.py"></a>

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

<a id="SQLite"></a>

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

<a id="sql-injection"></a>

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

<a id="cookie-and-session"></a>

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

<a id="decorator"></a>

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

<a id="endpoint-and-url">

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

<a id="template"></a>

## [テンプレート](https://msiz07-flask-docs-ja.readthedocs.io/ja/latest/tutorial/templates.html)
* テンプレートファイルは、flaskrパッケージ内のtemplatesディレクトリに格納する.
* テンプレートファイルとは、静的データと動的データのためのプレースホルダを含んでいるファイルである.
* テンプレートは、最終ドキュメントを作成するために特定のデータと一緒に変換（render）される.
* Flaskは、テンプレートの変換（render）にテンプレートライブラリのJinjaを使用する.
* Flaskでは、HTMLテンプレートの中で変換されるあらゆるデータを自動エスケープするようにJinjaが設定されている.<br>
-> ユーザが入力したデータを安全に表示できる（`<`や`>`のようなHTMLに干渉しかねない文字が入力されても、ブラウザの中では同じように見える安全な値へエスケープする）.
* ベースのテンプレートは、templatesディレクトリに直接置かれるが、blueprintのテンプレートは、templates下のblueprintと同じ名前のディレクトリに置かれる.
<br />

<a id="jinja"></a>

## [Jinja](https://shigeblog221.com/python-flask3/)
* Jinjaは、python用テンプレートエンジンの1つ.
* テンプレートエンジンは、ユーザの操作に合わせて、HTMLの内容を部分的に適した内容に書き換える仕組みで、テンプレートと呼ばれる雛形と、あるデータモデルで表現される入力データを合成し、ドキュメントを出力するソフトウェアである.
* Flaskをインストールすると、Jinja2も同時にインストールされる.
* [jinjaの使い方](https://www.sukerou.com/2019/04/jinja2flaskjinja2.html)
<br />

<a id="static-file">

## [静的ファイル](https://msiz07-flask-docs-ja.readthedocs.io/ja/latest/tutorial/static.html)
* HTMLレイアウトにスタイルを加えるために、CSSを追加することができる. スタイルは変化しないので、テンプレートファイルではなく、静的（static）ファイルになる.
* Flaskは、flaskr/staticディレクトリからの相対パスに対応するファイルのviewを自動的に追加する.
* CSSに加えて、他の種類の静的ファイルにロゴ画像やJavaScript関数のファイルがある場合、それらはすべてflaskr/staticディレクトリの下に置き、`url_for('staic', filename='...')`により参照できる.
<br />

<a id="can-install-project"></a>

## [プロジェクトをインストール可能にする](https://msiz07-flask-docs-ja.readthedocs.io/ja/latest/tutorial/install.html)
* プロジェクトをインストール可能にするということは、配布用（distribution）ファイルを作成でき、このプロジェクトの環境へFlaskをインストールしたときのように、その配布用ファイルを他の環境へインストールできることを意味する.
* `setup.py`ファイル
	```python
	from setuptools import find_packages, setup

	setup(
		name='flaskr',
		version='1.0.0',
		packages=find_packages(),
		include_package_data=True,
		zip_safe=False,
		install_requires=[
			'flask',
		],
	)
	```
		* プロジェクトと、プロジェクトに所属するファイルを記述する.
		* `packages`は、どのpackageディレクトリ（およびそれが含んでいるPythonファイル）を含めるべきかをPythonに伝える.
		* `find_packages()`は、packageディレクトリを全て手入力せずに済むように、packageディレクトリを自動的に見つけ出す.
		* staticやtemplatesディレクトリのような、（Pythonのpackageではない）その他のファイルを含めるには、`include_package_data`を設定する. そのようなその他のデータが何かを伝えるためには、Pythonは`MANIFEST.in`というもう一つのファイルを必要とする.
* `MANIFEST.in`ファイル
	```
	include flaskr/schema.sql
	graft flaskr/static
	graft flaskr/templates
	global-exclude *.pyc
	```
	* Pythonに、staticとtemplatesディレクトリにあるすべてと、schema.sqlファイルはコピーし、バイトコードのファイル（訳注：Pythonが実行時に作成・使用する中間ファイル）は除外するように伝える.
* [setup.pyとは](https://qiita.com/Tadahiro_Yamamura/items/2cbcd272a96bb3761cc8)
	* Pythonをインストールする際に標準で付属する`pip`を使用して、コードを他人と共有できる（特別な準備が不要）.
	* コードの共有方法
		```zsh
		pip install foopackage
		```
		* 上記コマンドを打ち込むだけで、依存関係も含めた環境を簡単に構築できる.
		* 上記のようにインストールしたパッケージは、コードに下記のように記述することでどこからでも参照できる.
			```python
			from foopackage.barmodule import hogehoge
			```
	* `setup.py`の例
		```python
		rom setuptools import setup

		setup(
			name="パッケージの名前",
			version="パッケージのバージョン(例:1.0.0)",
			install_requires=["packageA", "packageB"],
			extras_require={
				"develop": ["dev-packageA", "dev-packageB"]
			},
			entry_points={
				"console_scripts": [
					"foo = package_name.module_name:func_name",
					"foo_dev = package_name.module_name:func_name [develop]"
				],
				"gui_scripts": [
					"bar = gui_package_name.gui_module_name:gui_func_name"
				]
			}
		)
		```
		* 設定内容は、すべて`setup()`の引数として記述する.
		* `install_requires`で指定されたパッケージは、`pip install -e .`した時に一緒にインストールされる.
		* `extra_requires`で指定されたパッケージは、`pip install -e . [develop]`などと指定することでインストールされる.
		* `entry_points`に指定された関数は、`pip install`した時に実行可能ファイルとして生成される.
	* `setup.cfg`の利用
		* `setup.py`での設定項目が増えた場合には読みにくくなるので、`setup.py`と同じディレクトリに`setup.cfg`という設定ファイルを作成する方がよい.
	* `setup.cfg`を使用した`setup.py`の記述方法
		* `setup.py`
			```python
			from setuptools import setup

			setup()
			```
		* `setup.cfg`
			```
			# metadataセクションではパッケージのメタデータを定義する
			# これらの値はpypiで公開した際に表示される。
			# なおversion等、一部のキーはディレクティブの指定により外部ファイルから値を取得することができる
			# https://setuptools.readthedocs.io/en/latest/setuptools.html#metadata
			[metadata]
			name = your_package
			version = attr: src.VERSION
			license = file: license.txt

			# optionsセクションではパッケージの依存関係やpip installした時の動作を定義する
			# 値が複数ある場合、インデントすることで1行に1つの値を書くことができる。
			# https://setuptools.readthedocs.io/en/latest/setuptools.html#options
			[options]
			install_requires =
				packageA
				packageB

			# optionの内、値のTypeがsectionのものは別セクションで記述する。
			[options.extras_require]
			develop =
				dev_packageA
				dev_packageB

			[options.entry_points]
			console_scripts =
				foo = package_name.module_name:func_name
				foo_dev = package_name.module_name:func_name [develop]
			gui_scripts =
				bar = gui_package_name.gui_module_name:gui_func_name
			```
* [MANIFEST.inとは](https://qiita.com/airtoxin/items/2eafb930fa9b54ee7149)
	* デフォルトだとPythonファイルしかパッケージに入れてくれないので、その他のファイルを入れるためには`MANIFEST.in`が必要となる.
	* [MANIFEST.in を使ってソースコード配布物にファイルを含める](https://packaging.python.org/ja/latest/guides/using-manifest-in/)
	* [ソースコード配布物を作成する](https://docs.python.org/ja/3/distutils/sourcedist.html)
<br />

<a id="install-project"></a>

## [プロジェクトのインストール](https://msiz07-flask-docs-ja.readthedocs.io/ja/latest/tutorial/install.html)
* プロジェクトをインストールするには下記コマンドを実行する.
	```zsh
	pip install -e .
	```
	* このコマンドは、pipにカレントディレクトリからsetup.pyを見つけ出し、それを編集可能（editable）または開発（development）モードでインストールするように伝える.
	* 編集可能モードは、ローカルのコードを変更した時に、プロジェクトの依存対象のような、プロジェクトに関するメタデータを変更した場合だけ再インストールが必要なようにする.
<br />

<a id="test"></a>

## [テストの網羅率](https://msiz07-flask-docs-ja.readthedocs.io/ja/latest/tutorial/tests.html)
* アプリケーションに対してユニットテストを書くことで、書いたコードが期待通りに機能することをチェックできるようになる.
* Flaskは、アプリケーションへのリクエストをシミュレートしてレスポンスデータを返す、テスト用のクライアントを提供する.
* 可能な限り多くのコードをテストするべきである.
* 関数内のコードは、関数が呼び出された時だけ走り、ifブロックのような分岐箇所は条件が合った時だけ走る.
* 網羅率が100%に近づくほど、変更した時に変更箇所以外の振る舞いへ予想外の変化を起こさないという安心感がより得られる. しかしながら、100%の網羅率はアプリケーションにバグがないことを保証するわけではない. 特に、ユーザがブラウザの中でアプリケーションとどのようにやり取りするかについてはテストしない.
* コードのテストおよび網羅率の測定には、[pytest](https://docs.pytest.org/en/7.2.x/)と[coverage](https://coverage.readthedocs.io/en/7.2.2/)を使用する.
	```zsh
	pip install pytest coverage
	```
* Setup and Fixtures
	* テスト用コードは、`tests`ディレクトリに置く.
	* `tests`ディレクトリは、`flaskr`パッケージの中ではなく、同じ階層に置く.
	* `tests/confest.py`ファイルに書くテストで使用するfixturesと呼ばれるsetup関数を記述する.
	* テストに使用する自作Pythonモジュールとテスト関数の命名は、`test_`で始める.
	* テストで使用する一時的なデータベースを作成し、テスト中に使用するデータを挿入する.
* [pytest](https://rinatz.github.io/python-book/ch08-02-pytest/)
	* Pytestとは
		* Pythonの単体テストを書くためのフレームワークの1つ.
		* 他のフレームワークに、unitest（標準ライブラリ）、nose（かつての主流）などが存在するが、現在主流なのはpytestである.
	* 準備
		* 単体テストのソースコードは、`tests`ディレクトリ配下に作成する.
		* テストコードが1つで十分な場合は、ディレクトリを作成しなくてもよい.
	* パラメータ化したテスト
		* パラメータ化したテストは、テスト内で使用するパラメータを関数の引数として渡せるように書き直したテストのこと. 複数のパラメータでテストを実行できる.
		* パラメータ化したテストでテストを記述した場合は、すべてのパラメータのテストを実行するまでテストが続行される.
		* テストをパラメータ化するには、`@pytest.mark.parametrize()`を使用する. `@pytest.mark.parametrize()`は、デコレータであり、これにテストで使用するパラメータを記述する.
	* フィクスチャ
		* フィクスチャは、テストの実行前後で行いたい前処理/後処理を記述するために使用する関数のことである.
		* 各テストで同じ前処理/後処理を行う必要がある場合に、暗黙的にそれが実行されるようになる.
		* フィクスチャの構造
			```python
			@pytest.fixture
			def txt():
				# 前処理

				yield ...   # テスト関数に何らかの値を渡す

				# 後処理
			```
	* `conftest.py`
		* 複数のファイルをまたいで共通のフィクスチャを使用したい場合は、フィクスチャを`conftest.py`ファイルに定義する.
		* `conftest.py`ファイル内のフィクスチャは、pytestによって自動的にインポートされ、`conftest.py`ファイルがあるディレクトリ配下で暗黙的に参照できるようになる.
* テストの実行
	* 絶対に必要というわけではないが、coverageを使用したテストを実行する時は、テストメッセージの出力を絞るために、いくらかの追加設定をできる. その設定は、プロジェクトに`setup.cfg`ファイルを追加し、そのファイルの中に記述する.
	* テストを実行するには、`pytest`コマンドを使用する.
		```zsh
		pytest
		```
		* `pytest`コマンドは、ここまでで書いたテスト関数をすべて見つけ出して実行する.
		* [下記のエラーが表示された場合の解決策](https://yoshinorin.net/articles/2020/05/05/done-flask-tutorial/)
			```zsh
			tests/conftest.py:5: in <module>
    			from flaskr import create_app
			E   ModuleNotFoundError: No module named 'flaskr'
			```
			* `setup.py`が存在するディレクトリ内で、`pip install -e .`でローカルにパッケージングする.
		* `pytest -v`を実行すると、「.」が表示される代わりに、テスト関数の一覧が取得できる.
	* テストコードの網羅率を測定するには、pytestを直接実行する代わりに、`coverage`コマンドを使用してpytestを実行する.
		```zsh
		coverage run -m pytest
		```
<br />

<a id="deploy"></a>

## 本番環境へのデプロイ
* ビルドとインストール
	* どこかへ自分のアプリケーションをデプロイしたい場合は、配布ファイルをビルドする.
	* 現在の標準的なPythonの配布ファイルは、拡張子が`.whl`のwheel形式である.
		```zsh
		pip install wheel
		```
	* Pythonを使用して、`setup.py`を実行すると、ビルド関連のコマンドを行うコマンドラインツールになる. `bdist_wheel`コマンドは、wheel配布ファイルをビルドする.
		```zsh
		python setup.py bdist_wheel
		```
		* ビルドしたファイルは、`dist/flaskr-1.0.0-py3-none-any.whl`で見つけることができる.
		* ファイル名は、{project name}-{version}-{python tag}-{abi tag}-{platform tag}という形式になる.
	* ビルドしたwheelファイルを別のマシンにコピーし、仮想環境を準備し、pipを使用してそのファイルをインストールする.
		```zsh
		pip install flaskr-1.0.0-py3-none-any.whl
		```
	* 別のマシンでは、もう一度`init-db`を実行して、インスタンスフォルダにデータベースを作成する必要がある.
		```zsh
		flask --app flaskr init-db
		```
		* Flaskが編集可能モードではなく、インストールされていると検知した時は、Flaskはインスタンスフォルダにインストールされた場所とは別のディレクトリを使用する. それは、`venv/var/flaskr-instance`で見つけることができる.
* 秘密鍵の設定
	* チュートリアルの始めでは、SECRET_KEYへ標準設定の値を与えていたが、本番環境では規則性のないrandom byteへ変更するべきである. そうしないと、攻撃者が公開された`'dev'`に設定されているキーを使用してセッションのクッキーの変更や、その他の秘密鍵を使用したあらゆることをできるようになってしまう.
	* randomな秘密鍵を出力するには以下のコマンドが使用できる.
		```zsh
		python -c 'import secrets; print(secrets.token_hex())'
		```
* 本番環境サーバでの実行
	* 開発環境ではなく、公開されるようにFlaskを実行する時は、組み込みの開発サーバを使用（`flask run`）するべきではない.
	* 開発サーバは、便利なようにWerkzeugによって提供されているが、効率性、安定性、セキュリティを特別意識して設計されてはいない.
	* 公開する時は、本番環境の[WSGIサーバ](https://blog.hirokiky.org/entry/2018/09/30/183840)を使用する. 一例として、Waitressを使用するには、まずは仮想環境にインストールする.
		```zsh
		pip install waitress
		```
	* Waitressへ自分のアプリケーションについて伝える必要があるが、それは`flask run`のように`--app`を使用しない. Flaskアプリケーションのオブジェクトを取得するためには、application factoryをimportして呼び出すということをWaitressへ伝える必要がある.
		```zsh
		waitress-serve --call 'flaskr:create_app'
		```
	* [デプロイの詳細情報](https://msiz07-flask-docs-ja.readthedocs.io/ja/latest/deploying/index.html)
<a id="reference"></a>

## Reference
* [Tutorial](https://msiz07-flask-docs-ja.readthedocs.io/ja/latest/tutorial/index.html)

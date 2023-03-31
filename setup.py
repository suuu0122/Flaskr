from setuptools import find_packages, setup

'''
setup():
	packages:
		どのpackageディレクトリ（およびそれが含んでいるPythonファイル）を含めるべきかを
        Pythonに伝える.
    find_packages():
		packageディレクトリすべてを手入力せずに済むように、packageディレクトリを自動的に
        見つけ出す.
    include_package_data:
		staticやtemplatesディレクトリのような、その他のファイルを含めるには、include_package_data
        を設定する.
        そのようなその他のデータが何かを伝えるために、PythonはMANIFEST.inというもう1つの
        ファイルを必要とする.
'''
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
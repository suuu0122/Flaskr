from flaskr import create_app

'''
test_config():
    factory自身についてはテストする所はない.
    コードのほとんどは、各テストで実施されるため、何かに失敗している場合は他のテストで気づく.
    この関数は、テスト用設定を渡すための関数であり、もし設定が渡されない場合は何かしらの標準設定
    になっており、そうでなければ設定は上書きされる.
'''
def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing

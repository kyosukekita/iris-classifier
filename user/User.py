from flask_login import UserMixin

class User(UserMixin):
    # 追加
    # ユーザーが一意となるIDを取得できるメソッドが必要
    # 今回は無理やり1を渡す
    def get_id(self):
        return 1
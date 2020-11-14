from flask_login import UserMixin

from Dao.query import Util


class Login(UserMixin):

    @staticmethod
    def testLogin(username, password):
        session = Util.getDBSession("root", "chuanzhi", "bookstore")()
        print(session)
        account = Util.queryUserByUsername(username, session)
        session.close()
        if not account:
            return False
        if str(account.accountId) != password:
            return False
        return True

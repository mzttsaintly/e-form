
from hmac import compare_digest
from connect import get_password


def authenticate(user_name, password):
    """
    获取认证的回调函数，从request中获得登录凭证，返回凭证所代表的用户实体
    :param user_name: 用户名
    :param password: 输入的密码
    :return: User
    """
    user = get_password(user_name)
    if user and compare_digest(user.password.encode('utf-8'), password.encode('utf-8')):
        return user



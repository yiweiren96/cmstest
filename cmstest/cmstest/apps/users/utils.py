from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from users.models import User


def jwt_response_payload_handler(token, user=None, request=None):
    """
    自定义登录成功后返回给客户端的数据(字段)
    """
    return {
        'token': token,
        'user_id': user.id,
        'username': user.username
    }


class UsernameMobileAuthBackend(ModelBackend):
    """用户名移动认证后端,,自定义认证方式"""

    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        使用用户名或手机号登录
        :param request:
        :param username: 用户名 或者 手机号
        :param password: 密码
        :param kwargs:
        :return:
        """
        query_set = User.objects.filter(Q(username=username) | Q(mobile=username))
        try:
            if query_set.exists():  # 有查询到数据
                # 取出查询集中的用户对象
                user = query_set.get()

                if user.check_password(password):
                    # 用户名(手机号)密码正确
                    return user

        except:  # 用户名(手机号)密码不正确, 返回None
            return None


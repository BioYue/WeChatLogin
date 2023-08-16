from django.db import models
import time


class TextMsg:
    def __init__(self, to_user, from_user, recv_msg):
        self._toUser = to_user
        self._fromUser = from_user
        self._recvMsg = recv_msg
        self._nowTime = int(time.time())

    def structReply(self):
        text = """
                <xml>
                <ToUserName><![CDATA[{}]]></ToUserName>
                <FromUserName><![CDATA[{}]]></FromUserName>
                <CreateTime>{}</CreateTime>
                <MsgType><![CDATA[text]]></MsgType>
                <Content><![CDATA[{}]]></Content>
                </xml>
                """.format(self._fromUser, self._toUser, self._nowTime, self._recvMsg)  # 前面两个参数的顺序需要特别注意
        return text


class User(models.Model):
    openId = models.CharField(null=True, blank=True, max_length=200, verbose_name='用户唯一凭证')
    tmp_scene_str = models.CharField(null=True, blank=True, max_length=100, verbose_name='登录临时凭证')
    lastLoginTime = models.CharField(null=True, blank=True, max_length=50, verbose_name='最后登录时间')




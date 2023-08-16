from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
import xml.etree.ElementTree as ET
from django.utils import timezone
import requests
import hashlib
import uuid
import json

from app.models import TextMsg, User


appID = "wx8ac3xxx9236efe2a"
appSecret = "131b8d9d8xxx74afb751ce6b2"


class WeChatLogin(APIView):
    """
    微信登录
    """

    def get(self, request):
        qr_data = self.createShortTicket(str(uuid.uuid4()))
        qr_code_url = "https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket={}".format(qr_data[0])
        return Response({'url': qr_code_url, 'scene': qr_data[1]})

    def createShortTicket(self, scene_str):
        """
        生成短效二维码
        :param scene_str:
        :return:
        """
        print("scene_str-------{}".format(scene_str))
        url = "https://api.weixin.qq.com/cgi-bin/qrcode/create?access_token={}".format(self.getAccessToken())
        data = {
            "expire_seconds": 180,              # 二维码有效时间, 以秒为单位
            "action_name": "QR_STR_SCENE",      # 二维码类型, QR_STR_SCENE为临时的字符串参数值
            "action_info": {                    # 二维码详细信息
                "scene": {
                    "scene_str": scene_str      # 场景值ID（字符串形式的ID, 字符串类型, 长度限制为1到64
                }
            }
        }
        return [json.loads(requests.post(url, json=data).content.decode("utf-8")).get("ticket"), scene_str]

    def getAccessToken(self):
        """
        获取公众号全局接口调用凭证（有效期2h）
        建议公众号开发者使用中控服务器统一获取和刷新access_token
        """
        url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}' \
            .format(appID, appSecret)
        return requests.get(url).json().get('access_token')


class WeChatSignature(APIView):
    def get(self, request):
        signature = request.query_params.get("signature")
        timestamp = request.query_params.get("timestamp")
        nonce = request.query_params.get("nonce")
        yue_token = 'yueyue'
        sort_str = ''.join(sorted([yue_token, timestamp, nonce]))
        hash_str = hashlib.sha1(sort_str.encode()).hexdigest()
        if hash_str == signature:
            return HttpResponse(request.query_params.get("echostr"), content_type="text/html; charset=utf-8")
        else:
            return Response("Invalid signature", status=403)

    def post(self, request):
        """
        to_user_name: 公众号的微信号
        from_user_name: 发送方OpenId
        create_time：消息创建时间（时间戳）
        msg_type: 消息类型
        :return:
        """
        wx_data = request.body
        xml_data = ET.fromstring(wx_data)
        to_user_name = xml_data.find('ToUserName').text
        from_user_name = xml_data.find('FromUserName').text
        create_time = xml_data.find('CreateTime').text
        msg_type = xml_data.find('MsgType').text
        event_key = xml_data.find('EventKey').text
        print('---------------------------')
        print("EventKey---------{}".format(event_key))
        print('---------------------------')
        if msg_type == 'event':
            event = xml_data.find('Event').text
            print(event)
            if event == 'subscribe':
                tmp_scene_str = event_key.split('_')[1]
                scene_str = User.objects.filter(tmp_scene_str=tmp_scene_str)
                if not scene_str.exists():
                    ticket = xml_data.find('Ticket').text
                    print("ticket-----------{}".format(ticket))
                    datetime_obj = timezone.datetime.fromtimestamp(int(create_time))
                    create_time = datetime_obj.strftime('%Y-%m-%d %H:%M:%S')
                    new_user = User.objects.get_or_create(openId=from_user_name)[0]
                    new_user.tmp_scene_str = tmp_scene_str
                    new_user.lastLoginTime = create_time
                    new_user.save()
                    xml_text = TextMsg(to_user_name, from_user_name, '新用户--登录成功').structReply()
                else:
                    xml_text = TextMsg(to_user_name, from_user_name, '二维码已失效').structReply()
                return HttpResponse(xml_text)
            elif event == 'SCAN':
                scene_str = User.objects.filter(tmp_scene_str=event_key)
                if not scene_str.exists():
                    ticket = xml_data.find('Ticket').text
                    print("ticket-----------{}".format(ticket))
                    datetime_obj = timezone.datetime.fromtimestamp(int(create_time))
                    create_time = datetime_obj.strftime('%Y-%m-%d %H:%M:%S')
                    User.objects.filter(openId=from_user_name).update(tmp_scene_str=event_key, lastLoginTime=create_time)
                    xml_text = TextMsg(to_user_name, from_user_name, '老用户--登录成功').structReply()
                else:
                    xml_text = TextMsg(to_user_name, from_user_name, '二维码已失效').structReply()
                return HttpResponse(xml_text)
        xml_text = TextMsg(to_user_name, from_user_name, '服务器故障，请联系管理员或重试').structReply()
        return HttpResponse(xml_text)


class VerifyLogin(APIView):
    def get(self, request):
        scene_str = request.query_params.get('scene')
        tmp_scene_str = User.objects.filter(tmp_scene_str=scene_str)
        print('scene_str-----------{}------------'.format(scene_str))
        print('tmp_scene_str-----------{}------------'.format(tmp_scene_str))
        if tmp_scene_str:
            print('-------------登录成功!-------------')
            return Response('success')
        return Response({})

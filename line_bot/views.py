from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings


# 引入 linebot SDK
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import *


# 建立 linebot classs 進行連線
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)


@csrf_exempt
def callback(request):
    if (request.method == "POST"):
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        # 嘗試解密event
        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            print(event)
            if isinstance(event, MessageEvent):
                if isinstance(event.message, TextMessage):
                    res_text = event.message.text
                    # line_bot_api.reply_message(event.reply_token, TextSendMessage(text = res_text))
                    if res_text == "@我要報到":
                        # 回復貼圖訊息
                        line_bot_api.reply_message(event.reply_token, StickerSendMessage(package_id= 6325, sticker_id= 10979904))
                    elif res_text == "@我的名牌":
                        # 回復圖片訊息
                        img_url = "https://i.imgur.com/MouYR6ul.jpg"
                        line_bot_api.reply_message(event.reply_token, ImageSendMessage(original_content_url=img_url, preview_image_url=img_url))
                    elif res_text == "@車號登入":
                        # 地點訊息
                        line_bot_api.reply_message(event.reply_token, LocationSendMessage(title = "停車場", address="402台灣台中市南區仁義街119號", latitude=24.12355577054, longitude=120.6732894759063))
                    else:
                        line_bot_api.reply_message(event.reply_token, TextSendMessage(text = res_text))

                if isinstance(event.message, LocationMessage):
                    res_text = "{} {}".format(event.message.latitude, event.message.longitude)
                    print(event)
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text = res_text))

                if isinstance(event.message, ImageMessage):
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text = "這是一張圖片事件"))

        return HttpResponse()
    else:
        return HttpResponseBadRequest()


def pushMsg(request, uid):
    line_bot_api.push_message(uid, TextSendMessage(text="Hello"))
    return HttpResponse()

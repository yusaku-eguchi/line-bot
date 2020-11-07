from flask import Flask, request, abort
from linebot import(
    LineBotApi, WebhookHandler
)
import os

from linebot.exceptions import(
    InvalidSignatureError
)
from linebot.models import(
    MessageEvent, TextMessage, TextSendMessage, FollowEvent, UnfollowEvent
)

import getNikkeiHeikin

YOUR_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

def reply_message(event):
    # 日経平均株価の送信
    user_id = event.source.user_id
    NikkeiHeikin = getNikkeiHeikin.get_nikkei_heikin()
    messages = TextSendMessage(text="現在の日経平均株価は\n" + NikkeiHeikin + "円\nです")
    line_bot_api.push_message(user_id, messages=messages)
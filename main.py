# coding: UTF-8
import urllib.request, urllib.error

import csv
from datetime import datetime
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

#mysql接続用
import mysql.connector

#ログ出力のため
import logging
import sys

import AddUser
import DeleteUser
import ReplyMessage

app = Flask(__name__)

# ログを標準出力へ。heroku logs --tail で確認するためです。
# app.logger.info で出力するため、レベルは INFO にする。
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.INFO)

YOUR_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)


@app.route("/")
def hello_world():
   return "hello world!"

@app.route("/callback", methods=['POST'])
def callback():
   # get X-Line-Signature header value
   signature = request.headers['X-Line-Signature']

   # get request body as text
   body = request.get_data(as_text=True)
   app.logger.info("Request body: " + body)

   # handle webhook body
   try:
       handler.handle(body, signature)
   except InvalidSignatureError:
       print("Invalid signature. Please check your channel access token/channel secret.")
       abort(400)

   return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def reply(event):
    ReplyMessage.reply_message(event)


@handler.add(FollowEvent)
#友達追加時にuser情報保存
def forrow(event):
    AddUser.add_user(event)

@handler.add(UnfollowEvent)
#友達登録解除時にuser情報削除
def unfollow(event):
    DeleteUser.delete_user(event)

if __name__ == "__main__":
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)
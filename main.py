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

app = Flask(__name__)

# ログを標準出力へ。heroku logs --tail で確認するためです。
# app.logger.info で出力するため、レベルは INFO にする。
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.INFO)

YOUR_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]
USER_ID = '12971135132294'

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
def reply_message(event):
    # reply のテスト。
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='こちらこーるばっく処理からお送りします:'+event.message.text))
    user_id = event.source.user_id
    messages = TextSendMessage(text=f"こんにちは😁\n\n"
                                    f"最近はいかがお過ごしでしょうか?")
    line_bot_api.push_message(user_id, messages=messages)


@handler.add(FollowEvent)
#友達追加時にuser情報保存
def add_user(event):
    profile = line_bot_api.get_profile(event.source.user_id)
    user_id = profile.user_id
    display_name = profile.display_name
    status_message = profile.status_message
    db_connect = mysql.connector.connect(
        host = os.environ["DB_HOSTNAME"],
        port = '3306',
        user = os.environ["DB_USERNAME"],
        password = os.environ["DB_PASSWORD"],
        database = os.environ["DB_NAME"]
    )
    #カーソル呼出し
    db_curs = db_connect.cursor()

    #データ挿入SQL
    sql = 'Insert INTO heroku_610747411f1dc55.user(user_id, display_name, status_message) values(user_id, display_name, status_message)'
    db_curs.execute(sql)

    db_connect.commit()
    db_connect.close()

@handler.add(UnfollowEvent)
#友達登録解除時にuser情報削除
def delete_user(event):
    profile = line_bot_api.get_profile(event.source.user_id)
    db_connect = mysql.connector.connect(
        host = os.environ["DB_HOSTNAME"],
        port = '3306',
        user = os.environ["DB_USERNAME"],
        password = os.environ["DB_PASSWORD"],
        database = os.environ["DB_NAME"]
    )
    #カーソル呼出し
    db_curs = db_connect.cursor()

    #データ削除SQL
    sql = 'DELETE FROM user WHERE user_id = profile.user_id'
    db_curs.execute(sql)



if __name__ == "__main__":
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)
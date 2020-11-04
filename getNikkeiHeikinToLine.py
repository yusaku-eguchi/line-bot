# coding: UTF-8
import urllib.request, urllib.error
from bs4 import BeautifulSoup
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
    MessageEvent, TextMessage, TextSendMessage
)

#ログ出力のため
import logging
import sys

app = Flask(__name__)

# ログを標準出力へ。heroku logs --tail で確認するためです。
# app.logger.info で出力するため、レベルは INFO にする。
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.INFO)

YOUR_CHANNEL_ACCESS_TOKEN = '7daN8C8fvz/Mb614TwGrXSIPOA/rNYopIQHWtfpKWn6StPCG+/gVS0JhO38sMIx04OGqjS21IbKwXazaETM4BIQPjjNfzGNour2cUO7etCbYdHwGA5pbeLFmDBhgAHaujyFcJeUkKY0LGz7nMTAf3gdB04t89/1O/w1cDnyilFU='
YOUR_CHANNEL_SECRET = '13f10b72997410fab6886825485b561c'

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


if __name__ == "__main__":
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)
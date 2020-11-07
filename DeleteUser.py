#mysql接続用
import mysql.connector
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
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

def delete_user(event):
    user_id = event.source.user_id
    db_connect = mysql.connector.connect(
        host = os.environ["DB_HOSTNAME"],
        port = '3306',
        user = os.environ["DB_USERNAME"],
        password = os.environ["DB_PASSWORD"],
        database = os.environ["DB_NAME"]
    )
    print("接続完了")
    #カーソル呼出し
    db_curs = db_connect.cursor()

    #データ削除SQL
    sql = "DELETE FROM heroku_610747411f1dc55.users WHERE user_id = %s", (user_id)
    db_curs.execute("DELETE FROM heroku_610747411f1dc55.users WHERE user_id = %s", (user_id,))

    db_connect.commit()
    db_connect.close()
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
    sql = "INSERT INTO heroku_610747411f1dc55.users(user_id, name, status_message) VALUES (%s, %s, %s)", (user_id, display_name, status_message)
    db_curs.execute("INSERT INTO heroku_610747411f1dc55.users(user_id, name, status_message) VALUES (%s, %s, %s)", (user_id, display_name, status_message))

    db_connect.commit()
    db_connect.close()
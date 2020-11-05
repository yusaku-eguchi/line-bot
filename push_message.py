from linebot import LineBotApi
from linebot.models import TextSendMessage
import os

YOUR_CHANNEL_ACCESS_TOKEN = '7daN8C8fvz/Mb614TwGrXSIPOA/rNYopIQHWtfpKWn6StPCG+/gVS0JhO38sMIx04OGqjS21IbKwXazaETM4BIQPjjNfzGNour2cUO7etCbYdHwGA5pbeLFmDBhgAHaujyFcJeUkKY0LGz7nMTAf3gdB04t89/1O/w1cDnyilFU='
USER_ID = '12971135132294'

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)

line_bot_api.push_message(
    USER_ID,
    TextSendMessage(text='ぷっしゅめっせーじです。やあ!'))
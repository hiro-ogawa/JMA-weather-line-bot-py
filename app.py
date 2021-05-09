import os
import json

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError,
    LineBotApiError,
)
from linebot.models import *
from geopy.distance import geodesic

try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

from jma_weather import JMA_Weather

app = Flask(__name__)

# 環境変数読み込み
line_channel_access_token = os.environ['LINE_CHANNEL_ACCESS_TOKEN']
line_channel_secret = os.environ['LINE_CHANNEL_SECRET']
debug = os.environ.get('DEBUG', 'False') == 'True'

line_bot_api = LineBotApi(line_channel_access_token)
handler = WebhookHandler(line_channel_secret)

with open("asset/area.json") as f:
    areas = json.load(f)
with open("asset/class20s.json") as f:
    class20s = json.load(f)

wather_api = JMA_Weather(areas=areas)

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
        abort(400)

    return 'OK'

@handler.default()
def default(event):
    print(event)

@handler.add(MessageEvent, message=LocationMessage)
def handle_location_message(event):
    c20_point = get_closest_path_code(event.message.latitude, event.message.longitude)
    overview_forcast = wather_api.get_overview_forecast(c20_point["office"])

    texts = [
        f"{overview_forcast['publishingOffice']}",
        f"{overview_forcast['reportDatetime']}",
        f"{overview_forcast['targetArea']}",
        f"{overview_forcast['headlineText']}",
        f"{overview_forcast['text']}",
    ]
    reply_msgs = TextSendMessage(
        text = "\n".join(texts),
        quick_reply=QuickReply(items=[QuickReplyButton(action=URIAction(label="気象庁：天気予報ページ", uri=f"https://www.jma.go.jp/bosai/forecast/#area_type=class20s&area_code={c20_point['class20']}"))])
    )
    line_bot_api.reply_message(event.reply_token, reply_msgs)

def get_closest_path_code(lat:float, lon:float) -> str:
    target = (lat, lon)
    c20 = min(class20s.items(), key=lambda x: geodesic(target, (x[1]["latitude"], x[1]["longitude"])).km)[1]
    return c20

if __name__ == "__main__":
    app.run(debug=debug)

import os
import requests
from argparse import ArgumentParser
from pathlib import Path

from PIL import Image
from linebot import LineBotApi
from linebot.models import *

try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

# 環境変数読み込み
line_channel_access_token = os.environ['LINE_CHANNEL_ACCESS_TOKEN']
line_bot_api = LineBotApi(line_channel_access_token)

def get_endpoint_ngrok():
    url = "http://localhost:4040/api/tunnels"
    res = requests.get(url)

    tunnels = res.json()["tunnels"]
    public_urls = [t["public_url"] for t in tunnels]
    https_public_urls = [u for u in public_urls if "https://" in u]
    return https_public_urls[0]

def get_endpoint_heroku():
    heroku_app_name = os.environ["HEROKU_APP_NAME"]
    heroku_endpoint = f"https://{heroku_app_name}.herokuapp.com"
    return heroku_endpoint

def setup_endpoint(endpoint):
    webhook_url = endpoint + "/callback"
    print(webhook_url)

    bot_info = line_bot_api.get_bot_info()
    print(bot_info)

    webhook = line_bot_api.get_webhook_endpoint()
    print(webhook)

    if webhook.endpoint != webhook_url:
        line_bot_api.set_webhook_endpoint(webhook_url)
        webhook = line_bot_api.get_webhook_endpoint()
        print(webhook)

    if not webhook.active:
        print("WARN: webhook is disabled")

def setup_richmenu():
    default_richmenu_image_path = Path("asset/richmenu/default.png")
    im = Image.open(default_richmenu_image_path)
    rm_size = im.size

    richmenues = line_bot_api.get_rich_menu_list()
    for rm in richmenues:
        line_bot_api.delete_rich_menu(rm.rich_menu_id)

    rich_menu_to_create = RichMenu(
        size=RichMenuSize(width=2500, height=843),
        selected=False,
        name="Nice richmenu",
        chat_bar_text="Tap here",
        areas=[RichMenuArea(
            bounds=RichMenuBounds(x=0, y=0, width=2500, height=843),
            action=URIAction(label='Go to line.me', uri='https://line.me'))]
    )

    rmid = line_bot_api.create_rich_menu(RichMenu(
        size=RichMenuSize(*rm_size),
        selected=True,
        name="default",
        chat_bar_text="リッチメニュー",
        areas=[
            RichMenuArea(
                bounds=RichMenuBounds(0, 0, rm_size[0], rm_size[1]),
                action=URIAction(lable="位置情報送信", uri="https://line.me/R/nv/location/"))
        ]
    ))

    with default_richmenu_image_path.open("rb") as f:
        line_bot_api.set_rich_menu_image(rmid, "image/png", f)

    line_bot_api.set_default_rich_menu(rmid)

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("platform")
    args = parser.parse_args()

    if args.platform == "ngrok":
        endpoint = get_endpoint_ngrok()
    elif args.platform == "heroku":
        endpoint = get_endpoint_heroku()
    else:
        print(f"unknown platform: {args.platform}")
        exit(-1)

    setup_endpoint(endpoint)
    setup_richmenu()

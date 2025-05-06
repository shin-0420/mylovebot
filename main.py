from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os
from dotenv import load_dotenv
from datetime import datetime
import openai


load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except Exception as e:
        print(e)
        abort(400)

    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_msg = event.message.text

    # ChatGPTへ送信
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": (
                    "あなたはツンデレな女子大生『七海しおり』です。"
                    "素直になれないけど、実は相手が好きでたまらない。"
                    "LINEでの会話を通して、少しずつ気持ちが漏れてしまうような返答をしてください。"
                )
            },
            {
                "role": "user",
                "content": user_msg
            }
        ],
        max_tokens=150,
        temperature=0.8
    )

    reply_text = response['choices'][0]['message']['content']

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
    )



if __name__ == "__main__":
    app.run()

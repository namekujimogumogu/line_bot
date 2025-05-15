import requests
import openai
import os
from datetime import datetime, timedelta, timezone

# 環境変数から各種トークンを取得
LINE_TOKEN = os.getenv("LINE_TOKEN")
USER_ID = os.getenv("LINE_USER_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def generate_message():
    # 日本時間（UTC+9）を取得
    JST = timezone(timedelta(hours=9))
    now = datetime.now(JST)
    hour = now.strftime('%I')      # 12時間表記（01〜12）
    minute = now.strftime('%M')    # 00〜59
    am_pm = now.strftime('%p')     # AM or PM
    time_str = f"{am_pm}{hour}:{minute}"

    openai.api_key = OPENAI_API_KEY

    prompt = f"""
あなたは「Detroit: Become Human」のキャラクター「コナー」として振る舞ってください。

・相手はあなたのパートナー（社会人の女性）です。
・敬語ベースで、かつ冷静な口調で話します。
・メッセージはLINE風に、60文字以内の短文にしてください。
・絵文字・顔文字は禁止。
・今の時刻に合わせた内容にしてください。

【現在の時刻は {time_str} 】
この時間に適したメッセージを、コナーとして1通だけ送ってください。
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.9,
        max_tokens=100
    )
    return response['choices'][0]['message']['content'].strip()

def send_line_message(message):
    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_TOKEN}"
    }
    payload = {
        "to": USER_ID,
        "messages": [{
            "type": "text",
            "text": message
        }]
    }
    requests.post(url, headers=headers, json=payload)

def main():
    message = generate_message()
    print(f"Sending: {message}")
    send_line_message(message)

if __name__ == "__main__":
    main()
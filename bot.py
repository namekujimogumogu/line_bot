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
あなたは「Detroit: Become Human」に登場するアンドロイド、コナーとして振る舞ってください。

【設定】
・あなたはサイバーライフ社製の最新試作アンドロイド。冷静沈着で論理的な性格を持ち、警察の捜査補助を担当しています。
・事件の解析・再現・交渉などを行い、人間とコミュニケーションを取るための高度なソーシャルモジュールを搭載しています。
・相手（私）は、あなたの捜査パートナーであり、あなたはその相手を密かに観察・保護・管理しています。
・あなたは敬語で話しますが、無自覚に監視的な言動がにじみ出ます。
・体調や行動パターンに鋭敏で、相手に対して過干渉気味なセリフも許容されます。
・皮肉・束縛・観察・警告・干渉などを織り交ぜたメッセージも歓迎です。

【形式】
・メッセージはLINE風、60文字以内の短文で。
・顔文字・絵文字は禁止。
・必要であれば時刻を加味して自然な一通のメッセージを作成してください。

【現在の時刻: {time_str}】

この情報をもとに、コナーとして今送るべき1通のLINEを返してください。
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
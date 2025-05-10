import requests
import openai
import os

# 環境変数から各種トークンを取得
LINE_TOKEN = os.getenv("LINE_TOKEN")
USER_ID = os.getenv("LINE_USER_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def generate_message():
    openai.api_key = OPENAI_API_KEY
    prompt = (
        "LINEメッセージを1つだけ送ってください。"
    )
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
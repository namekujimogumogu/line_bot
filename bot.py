import openai
import requests
import os

def generate_message():
    openai.api_key = os.getenv("OPENAI_API_KEY")
    prompt = (
        "LINEメッセージを1つ生成してください。"
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
        "Authorization": f"Bearer {os.getenv('LINE_TOKEN')}"
    }
    payload = {
        "to": os.getenv("LINE_USER_ID"),
        "messages": [{
            "type": "text",
            "text": message
        }]
    }
    response = requests.post(url, headers=headers, json=payload)
    print("LINE Response:", response.status_code, response.text)

if __name__ == "__main__":
    msg = generate_message()
    print("Generated message:", msg)
    send_line_message(msg)
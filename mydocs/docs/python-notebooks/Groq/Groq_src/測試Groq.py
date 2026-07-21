from dotenv import load_dotenv
from groq import Groq

# 讀取 .env
load_dotenv()


client = Groq()
completion = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[
      {
        "role": "system", # 系統提示詞
        "content": ""
      },
      {
        "role": "user", # 使用者提示詞
        "content": "你好呀"
      }
    ],
    temperature=1,
    max_completion_tokens=1024,
    top_p=1,
    stream=True,
    stop=None
)

for chunk in completion:
    print(chunk.choices[0].delta.content or "", end="")

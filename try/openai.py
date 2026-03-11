from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

messages = [
    {"role": "system", "content": "你是一个人工智能助手，名字叫小梅梅，协助用户完成任务，并且不说废话简单回答。"},
    {"role": "user", "content": "告诉我你的名字是什么？"},
    ]

completion = client.chat.completions.create(
    model="qwen3.5-plus",  # 您可以按需更换为其它深度思考模型
    messages=messages,
    extra_body={"enable_thinking": False},
    stream=True,  
)



#流式输出
for chunk in completion:
    if chunk.choices[0].delta.content:
        print(
            chunk.choices[0].delta.content, 
            end="",
            flush=True # 确保实时输出（立刻刷新缓冲区）
            )